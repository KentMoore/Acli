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
MAX_PAGE = 332   # 总页数
BASE_URL = 'https://www.lanqiao.cn/problems/?first_category_id=1&sort=students_count&page={}'
MAX_WORKERS = 4  # 同时开的“标签页线程”数量，建议 2~6 之间试
OUTPUT_CSV = 'lanqiao_problems_all_drission_async.csv'


def split_pages(max_page: int, n_workers: int):
    """把 1..max_page 均匀分成 n_workers 份"""
    pages = list(range(1, max_page + 1))
    n_workers = min(n_workers, len(pages))
    size = math.ceil(len(pages) / n_workers)
    return [pages[i:i + size] for i in range(0, len(pages), size)]


def crawl_pages(tab, pages_subset):
    """
    在一个线程里使用一个标签页(tab)采集若干页。
    tab: ChromiumTab 或 ChromiumPage 对象
    """
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] 启动，负责页码：{pages_subset[0]} ~ {pages_subset[-1]}")

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
                # 官方说明：ContextLostError 是“页面被刷新”，需要等待后重试 :contentReference[oaicite:2]{index=2}
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

    print(f"[{thread_name}] 结束，抓到 {len(all_rows)} 条记录")
    return all_rows


def create_tabs(page: ChromiumPage, n_workers: int):
    """
    按官网“多线程操作标签页”的写法，在一个浏览器里开多个标签页，每个线程用一个。:contentReference[oaicite:3]{index=3}
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
    page_splits = split_pages(MAX_PAGE, MAX_WORKERS)
    num_workers = len(page_splits)
    print(f"总页数 {MAX_PAGE}，拆成 {num_workers} 个任务。")

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


def save_to_csv(all_batches):
    # 展开二维列表
    rows = [row for batch in all_batches for row in batch]

    # 按 (页码, 题号) 排序，保证顺序稳定
    rows.sort(key=lambda x: (x[0], int(x[1]) if str(x[1]).isdigit() else 999999))

    print("-" * 80)
    print(f"汇总后共 {len(rows)} 道题目，开始写入 CSV：{OUTPUT_CSV}")

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['序号', '题号', '题目名称', '难度', '通过率', '挑战人数', '标签', '所在页码'])

        for idx, (page_no, pid, title, level, percent, users, tag_str) in enumerate(rows, start=1):
            writer.writerow([idx, pid, title, level, percent, users, tag_str, page_no])

    print("💾 写入完成！")


if __name__ == '__main__':
    t0 = time.time()
    print("开始多线程 + asyncio 抓取蓝桥题目列表...")

    # ✅ 只创建一个页面对象，后面所有线程都通过不同 tab 来用它
    page = ChromiumPage()

    try:
        batches = asyncio.run(async_crawl_all(page))
        save_to_csv(batches)
    finally:
        # ✅ 只在主线程统一 quit 一次
        try:
            page.quit()
        except Exception:
            pass

    t1 = time.time()
    print(f"全部完成，用时 {t1 - t0:.2f} 秒")
