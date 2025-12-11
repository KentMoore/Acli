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

MAX_WORKERS = 4        # 列表页 线程 / 标签页 数量
DETAIL_WORKERS = 4     # 详情页 线程 / 标签页 数量
OUTPUT_CSV = 'lanqiao_problems_fulltext.csv'   # 输出文件名


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


def get_page_full_text(tab):
    """
    尽量获取【题目主要区域】的所有文本；
    如果定位不到，就退而求其次拿整个 body 的文本，再不行就 html 原文。
    """
    # 先试一些可能的“主体容器”
    candidate_selectors = [
        'div.problem-main',
        'div.problem-detail',
        'div.problem',          # 蓝桥经常用 problem 这个类
        'main',
        'div.main',
        'div.layout-main',
    ]

    for sel in candidate_selectors:
        try:
            ele = tab.ele(f'css:{sel}', timeout=0.8)
            if ele:
                txt = (ele.text or '').strip()
                # 太短说明不是正文，继续找
                if txt and len(txt) > 50:
                    return txt
        except Exception:
            pass

    # 退而求其次：整个 body 文本
    try:
        body = tab.ele('tag:body', timeout=1.5)
        if body:
            txt = (body.text or '').strip()
            if txt:
                return txt
    except Exception:
        pass

    # 最后兜底：整页 HTML（可能有标签，要你后处理）
    try:
        html = (tab.html or '').strip()
        return html
    except Exception:
        return ''


# ========================
# 第一阶段：抓取题目列表
# ========================
def crawl_pages(tab, pages_subset):
    """
    在一个线程里使用一个标签页(tab)采集若干页列表。
    """
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] 列表线程启动，负责页码：{pages_subset[0]} ~ {pages_subset[-1]}")

    all_rows = []

    for p in pages_subset:
        url = BASE_URL.format(p)

        # 每一页最多重试 3 次
        for attempt in range(1, 4):
            try:
                print(f"[{thread_name}] 抓取第 {p} 页 (第 {attempt} 次尝试)：{url}")
                tab.get(url)
                tab.wait.doc_loaded()
                time.sleep(0.8)

                items = tab.eles('css:div.problem-item-wrapper')
                if not items:
                    print(f"[{thread_name}] ⚠️ 第 {p} 页没有抓到任何题目（可能未登录/风控/页数超出）")
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
                break  # 当前页已成功，无需重试

            except ContextLostError:
                print(f"[{thread_name}] ⚠️ 第 {p} 页 ContextLostError，准备重试...")
                time.sleep(1.5)
                if attempt == 3:
                    print(f"[{thread_name}] ❌ 第 {p} 页重试 3 次仍失败，跳过。")

            except Exception as e:
                print(f"[{thread_name}] ❌ 第 {p} 页异常：{e}")
                if attempt == 3:
                    print(f"[{thread_name}] ❌ 第 {p} 页重试 3 次仍失败，跳过。")
                else:
                    time.sleep(1.5)

    print(f"[{thread_name}] 列表线程结束，共抓 {len(all_rows)} 条。")
    return all_rows


def create_tabs(page: ChromiumPage, n_workers: int):
    """
    在一个浏览器里开多个标签页，每个线程用一个。
    """
    tabs = []

    # 当前这个 page 的 tab 也拿来用
    tab0 = page.get_tab()
    tabs.append(tab0)

    # 再新建标签页
    for _ in range(n_workers - 1):
        tab_id = page.new_tab('about:blank')
        tab = page.get_tab(tab_id)
        tabs.append(tab)

    return tabs


async def async_crawl_all(page: ChromiumPage):
    """异步调度 + 线程池，抓完所有列表页"""
    page_splits = split_pages(MAX_PAGE, MAX_WORKERS)
    num_workers = len(page_splits)
    print(f"总页数 {MAX_PAGE}，拆成 {num_workers} 个列表任务。")

    tabs = create_tabs(page, num_workers)

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        tasks = [
            loop.run_in_executor(executor, crawl_pages, tabs[i], subset)
            for i, subset in enumerate(page_splits)
        ]
        all_batches = await asyncio.gather(*tasks)

    # 关掉多开的 tab（第一个是 page 本身，可以保留）
    for t in tabs[1:]:
        try:
            t.close()
        except Exception:
            pass

    return all_batches


def flatten_batches_to_problems(all_batches):
    """
    展开批次，变成方便后续处理的题目列表（dict 列表）
    """
    rows = [row for batch in all_batches for row in batch]
    # 按 (页码, 题号) 排个序
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
                'detail_url': DETAIL_URL.format(pid=pid) if pid else '',
                'full_text': '',   # 第二阶段填
            }
        )
    return problems


# ========================
# 第二阶段：抓取题目详情全文
# ========================
def crawl_detail_batch(tab, problems_subset):
    """
    在一个线程里用一个标签页抓若干题目的详情全文。
    """
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] 详情线程启动，要抓 {len(problems_subset)} 道题。")

    for problem in problems_subset:
        pid = problem['pid']
        if not pid:
            continue

        url = problem['detail_url'] or DETAIL_URL.format(pid=pid)
        problem['detail_url'] = url

        for attempt in range(1, 4):
            try:
                print(f"[{thread_name}] 抓取题号 {pid} (第 {attempt} 次)：{url}")
                tab.get(url)
                tab.wait.doc_loaded()
                time.sleep(0.8)

                full_text = get_page_full_text(tab)
                problem['full_text'] = full_text

                break   # 成功就退出重试循环

            except ContextLostError:
                print(f"[{thread_name}] ⚠️ 题号 {pid} ContextLostError，准备重试...")
                time.sleep(1.5)
                if attempt == 3:
                    print(f"[{thread_name}] ❌ 题号 {pid} 重试 3 次仍失败，跳过。")

            except Exception as e:
                print(f"[{thread_name}] ❌ 抓题号 {pid} 异常：{e}")
                if attempt == 3:
                    print(f"[{thread_name}] ❌ 题号 {pid} 重试 3 次仍失败，跳过。")
                else:
                    time.sleep(1.5)

    print(f"[{thread_name}] 详情线程结束。")
    return problems_subset


def crawl_all_details(page: ChromiumPage, problems, max_workers: int = DETAIL_WORKERS):
    """
    多线程 + 多标签页，抓所有题目的详情全文。
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

    # 关掉多开的 tab
    for t in tabs[1:]:
        try:
            t.close()
        except Exception:
            pass

    merged = [item for batch in results for item in batch]
    merged.sort(key=lambda x: x['idx'])
    return merged


# ========================
# 保存到 CSV
# ========================
def save_to_csv(problems):
    print("-" * 80)
    print(f"汇总后共 {len(problems)} 道题目（含全文），写入 CSV：{OUTPUT_CSV}")

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)

        # 注意：full_text 这一列会有很多换行，CSV 会自动加引号包起来
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
                'full_text',  # 题目详情页的所有文本
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
                    item['detail_url'],
                    item.get('full_text', ''),
                ]
            )

    print("💾 写入完成！")


# ========================
# 主入口
# ========================
if __name__ == '__main__':
    t0 = time.time()
    print("开始多线程 + asyncio 抓取蓝桥题目【列表 + 详情全文】...")

    page = ChromiumPage()   # 使用你本机的浏览器配置，确保已登录蓝桥

    try:
        # 第一阶段：列表页
        list_batches = asyncio.run(async_crawl_all(page))
        problems = flatten_batches_to_problems(list_batches)

        # 第二阶段：题目详情全文
        problems = crawl_all_details(page, problems)

        # 保存到 CSV
        save_to_csv(problems)

    finally:
        try:
            page.quit()
        except Exception:
            pass

    t1 = time.time()
    print(f"全部完成，用时 {t1 - t0:.2f} 秒")
