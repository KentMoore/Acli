from concurrent.futures import ThreadPoolExecutor
import asyncio
import csv
import math
import threading
import time

from DrissionPage import ChromiumPage
from DrissionPage.errors import ContextLostError

# ========================
# 配置
# ========================
MAX_PAGE = 332   # 列表总页数
BASE_URL = 'https://www.lanqiao.cn/problems/?first_category_id=1&sort=students_count&page={}'
DETAIL_URL = 'https://www.lanqiao.cn/problems/{pid}/learning/?page=1&first_category_id=1'

MAX_WORKERS = 4          # 列表页“标签页线程”数量
DETAIL_WORKERS = 4       # 题面详情的“标签页线程”数量，可与 MAX_WORKERS 相同
OUTPUT_CSV = 'lanqiao_problems_all_with_detail.csv'   # 输出文件名，避免覆盖你之前的 CSV


# ========================
# 工具函数
# ========================
def split_pages(max_page: int, n_workers: int):
    """把 1..max_page 均匀分成 n_workers 份"""
    pages = list(range(1, max_page + 1))
    n_workers = min(n_workers, len(pages))
    size = math.ceil(len(pages) / n_workers)
    return [pages[i:i + size] for i in range(0, len(pages), size)]


def split_list(items, n_workers: int):
    """通用列表切分，用于按题目切分详情任务"""
    if not items:
        return []

    n_workers = min(n_workers, len(items))
    size = math.ceil(len(items) / n_workers)
    return [items[i:i + size] for i in range(0, len(items), size)]


def safe_pick_text(tab, selectors, timeout=0.5):
    """
    依次尝试多个 CSS 选择器，返回第一个非空的 .text
    这里的 selectors 是一个列表，比如 ['div.problem-desc', 'div.problem-content']。
    """
    for sel in selectors:
        try:
            ele = tab.ele(f'css:{sel}', timeout=timeout)
            if ele:
                txt = (ele.text or '').strip()
                if txt:
                    return txt
        except Exception:
            # 某些选择器找不到元素会抛异常，忽略继续试下一个
            pass
    return ''


# ========================
# 第一阶段：抓取题目列表
# ========================
def crawl_pages(tab, pages_subset):
    """
    在一个线程里使用一个标签页(tab)采集若干页。
    tab: ChromiumTab 或 ChromiumPage 对象
    """
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] 列表线程启动，负责页码：{pages_subset[0]} ~ {pages_subset[-1]}")

    all_rows = []

    for p in pages_subset:
        url = BASE_URL.format(p)

        # 每一页最多重试 3 次，防止 ContextLostError 直接把程序干崩
        for attempt in range(1, 4):
            try:
                print(f"[{thread_name}] 抓取第 {p} 页 (第 {attempt} 次尝试)：{url}")
                tab.get(url)
                tab.wait.doc_loaded()   # 等页面加载完成
                time.sleep(0.8)         # 稍微歇一下，避免太猛触发风控

                items = tab.eles('css:div.problem-item-wrapper')
                if not items:
                    print(f"[{thread_name}] ⚠️ 第 {p} 页没有抓到任何题目（可能是未登录/风控/页数超出）")
                    break

                print(f"[{thread_name}] ✅ 第 {p} 页共 {len(items)} 道题")

                page_rows = []

                for item in items:
                    # 题号
                    id_ele = item.ele('css:span.problem-id', timeout=0)
                    pid = id_ele.text.strip() if id_ele else ''

                    # 题目名称
                    title_ele = item.ele('css:span.name.is-open', timeout=0)
                    if title_ele:
                        title = (title_ele.attr('title') or title_ele.text or '').strip()
                    else:
                        title = ''

                    # 难度
                    level_ele = item.ele('css:span.level-text', timeout=0)
                    level = level_ele.text.strip() if level_ele else '未知'

                    # 通过率
                    percent_ele = item.ele('css:span.meta-percent', timeout=0)
                    percent = percent_ele.text.strip() if percent_ele else '未知'

                    # 挑战人数
                    user_ele = item.ele('css:span.meta-users', timeout=0)
                    users = user_ele.text.strip() if user_ele else '未知'

                    # 标签
                    tag_eles = item.eles('css:div.problem-tags span.tag')
                    tags = [t.text.strip() for t in tag_eles]
                    tag_str = '、'.join(tags) if tags else ''

                    page_rows.append((p, pid, title, level, percent, users, tag_str))

                all_rows.extend(page_rows)
                # 当前页成功了就跳出重试循环
                break

            except ContextLostError:
                # 官方说明：ContextLostError 是“页面被刷新”，需要等待后重试
                print(f"[{thread_name}] ⚠️ 第 {p} 页出现 ContextLostError，可能是页面刷新了，准备重试...")
                time.sleep(1.5)

                if attempt == 3:
                    print(f"[{thread_name}] ❌ 第 {p} 页重试 3 次仍失败，跳过该页。")

            except Exception as e:
                print(f"[{thread_name}] ❌ 第 {p} 页出现其他异常：{e}")
                if attempt == 3:
                    print(f"[{thread_name}] ❌ 第 {p} 页重试 3 次仍失败，跳过该页。")
                else:
                    time.sleep(1.5)

    print(f"[{thread_name}] 列表线程结束，抓到 {len(all_rows)} 条记录")
    return all_rows


def create_tabs(page: ChromiumPage, n_workers: int):
    """
    在一个浏览器里开多个标签页，每个线程用一个。
    """
    tabs = []

    # 第一个标签页：当前这个 page 本身就可以当作一个 tab 使用
    tab0 = page.get_tab()
    tabs.append(tab0)

    # 再新建标签页
    for _ in range(n_workers - 1):
        # new_tab 返回的是 tab 的 id，这里先建空白页，后续线程里再 get 实际 URL
        tab_id = page.new_tab('about:blank')
        tab = page.get_tab(tab_id)
        tabs.append(tab)

    return tabs


async def async_crawl_all(page: ChromiumPage):
    """异步调度 + 线程池，抓完所有列表页"""
    page_splits = split_pages(MAX_PAGE, MAX_WORKERS)
    num_workers = len(page_splits)
    print(f"总页数 {MAX_PAGE}，拆成 {num_workers} 个列表任务。")

    # 按任务数创建对应数量的标签页
    tabs = create_tabs(page, num_workers)

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        tasks = [
            loop.run_in_executor(executor, crawl_pages, tabs[i], subset)
            for i, subset in enumerate(page_splits)
        ]
        all_batches = await asyncio.gather(*tasks)

    # 统一关掉多开的标签页（第一个 tab 就是 page，可以留着也无所谓）
    for t in tabs[1:]:
        try:
            t.close()
        except Exception:
            pass

    return all_batches


def flatten_batches_to_problems(all_batches):
    """
    把二维批次 all_batches 展平成按题号排序的题目列表，
    并转成 dict 结构，方便后面填充题目详情。
    """
    # 展开二维列表
    rows = [row for batch in all_batches for row in batch]

    # 按 (页码, 题号) 排序，保证顺序稳定
    rows.sort(key=lambda x: (x[0], int(x[1]) if str(x[1]).isdigit() else 999999))

    problems = []
    for idx, (page_no, pid, title, level, percent, users, tag_str) in enumerate(rows, start=1):
        problems.append(
            {
                'idx': idx,
                'page_no': page_no,
                'pid': pid,
                'title': title,
                'level': level,
                'percent': percent,
                'users': users,
                'tags': tag_str,
                # 以下字段第二阶段再填
                'detail_url': '',
                'desc': '',
                'input_desc': '',
                'output_desc': '',
                'sample_input': '',
                'sample_output': '',
            }
        )

    return problems


# ========================
# 第二阶段：抓取题目详情（题面）
# ========================
def parse_problem_detail(tab):
    """
    从【题目详情页】提取题目描述、输入输出说明、样例等。

    ⚠️ 注意：下面这些 CSS 选择器是根据常见结构猜的，
    如果抓到的内容为空，你可以：
      1. 手动打开一个题目页面（比如 20512）;
      2. F12 查看“题目描述”“输入说明”等所在的 div 的 class；
      3. 把对应 class 名补进下面的 selectors 列表里。
    """

    # 题目描述
    desc = safe_pick_text(
        tab,
        [
            'div.problem-desc',
            'div.problem-content',
            'div.desc',
            'div.markdown-body',
            'section.problem-content',
        ]
    )

    # 输入说明
    input_desc = safe_pick_text(
        tab,
        [
            'div.problem-input',
            'section.problem-input',
            'div.input-spec',
            'div.input > pre',
        ]
    )

    # 输出说明
    output_desc = safe_pick_text(
        tab,
        [
            'div.problem-output',
            'section.problem-output',
            'div.output-spec',
            'div.output > pre',
        ]
    )

    # 样例输入
    sample_input = safe_pick_text(
        tab,
        [
            'pre.sample-input',
            'div.sample-input pre',
            'code.sample-input',
        ]
    )

    # 样例输出
    sample_output = safe_pick_text(
        tab,
        [
            'pre.sample-output',
            'div.sample-output pre',
            'code.sample-output',
        ]
    )

    return desc, input_desc, output_desc, sample_input, sample_output


def crawl_detail_batch(tab, problems_subset):
    """
    在一个线程里使用一个标签页(tab)采集若干【题目详情页】。
    """
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] 详情线程启动，要抓 {len(problems_subset)} 道题目。")

    for problem in problems_subset:
        pid = problem['pid']
        if not pid:
            continue

        url = DETAIL_URL.format(pid=pid)
        problem['detail_url'] = url

        for attempt in range(1, 4):
            try:
                print(f"[{thread_name}] 抓取题号 {pid} 的题面 (第 {attempt} 次尝试)：{url}")
                tab.get(url)
                tab.wait.doc_loaded()
                time.sleep(0.8)  # 视情况可调小或调大

                desc, input_desc, output_desc, sample_in, sample_out = parse_problem_detail(tab)

                problem['desc'] = desc
                problem['input_desc'] = input_desc
                problem['output_desc'] = output_desc
                problem['sample_input'] = sample_in
                problem['sample_output'] = sample_out

                # 正常抓到就 break
                break

            except ContextLostError:
                print(f"[{thread_name}] ⚠️ 题号 {pid} 出现 ContextLostError，准备重试...")
                time.sleep(1.5)
                if attempt == 3:
                    print(f"[{thread_name}] ❌ 题号 {pid} 重试 3 次仍失败，跳过该题目。")

            except Exception as e:
                print(f"[{thread_name}] ❌ 抓取题号 {pid} 时出现异常：{e}")
                if attempt == 3:
                    print(f"[{thread_name}] ❌ 题号 {pid} 重试 3 次仍失败，跳过该题目。")
                else:
                    time.sleep(1.5)

    print(f"[{thread_name}] 详情线程结束。")
    return problems_subset


def crawl_all_details(page: ChromiumPage, problems, max_workers: int = DETAIL_WORKERS):
    """
    多线程 + 多标签页，把每道题的【题面详情】抓出来，填回 problems 列表。
    """
    if not problems:
        return problems

    splits = split_list(problems, max_workers)
    num_workers = len(splits)
    print(f"共 {len(problems)} 道题，拆成 {num_workers} 个详情任务。")

    tabs = create_tabs(page, num_workers)

    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(crawl_detail_batch, tabs[i], subset)
            for i, subset in enumerate(splits)
        ]
        for fut in futures:
            results.append(fut.result())

    # 统一关掉多开的标签页（第一个 tab 就是 page，可以留着也无所谓）
    for t in tabs[1:]:
        try:
            t.close()
        except Exception:
            pass

    # 合并结果，并按原 idx 排序
    merged = [item for batch in results for item in batch]
    merged.sort(key=lambda x: x['idx'])
    return merged


# ========================
# 保存到 CSV
# ========================
def save_to_csv(problems):
    print("-" * 80)
    print(f"汇总后共 {len(problems)} 道题目（含题面），开始写入 CSV：{OUTPUT_CSV}")

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                '序号',
                '题号',
                '题目名称',
                '难度',
                '通过率',
                '挑战人数',
                '标签',
                '所在页码',
                '题目链接',
                '题目描述',
                '输入说明',
                '输出说明',
                '样例输入',
                '样例输出',
            ]
        )

        for item in problems:
            writer.writerow(
                [
                    item['idx'],
                    item['pid'],
                    item['title'],
                    item['level'],
                    item['percent'],
                    item['users'],
                    item['tags'],
                    item['page_no'],
                    item.get('detail_url') or DETAIL_URL.format(pid=item['pid']),
                    item.get('desc', ''),
                    item.get('input_desc', ''),
                    item.get('output_desc', ''),
                    item.get('sample_input', ''),
                    item.get('sample_output', ''),
                ]
            )

    print("💾 写入完成！")


# ========================
# 主入口
# ========================
if __name__ == '__main__':
    t0 = time.time()
    print("开始多线程 + asyncio 抓取蓝桥题目【列表 + 题面】...")

    # 只创建一个页面对象，后面所有线程都通过不同 tab 来用它
    page = ChromiumPage()

    try:
        # 第一阶段：列表页
        list_batches = asyncio.run(async_crawl_all(page))
        problems = flatten_batches_to_problems(list_batches)

        # 第二阶段：题目详情页（题面）
        problems = crawl_all_details(page, problems)

        # 保存到 CSV
        save_to_csv(problems)

    finally:
        # 只在主线程统一 quit 一次
        try:
            page.quit()
        except Exception:
            pass

    t1 = time.time()
    print(f"全部完成，用时 {t1 - t0:.2f} 秒")
