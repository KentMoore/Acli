#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
抖音视频合集下载器 - 最终版
优化API响应收集和视频处理逻辑
"""

import requests
import os
import re
import json
from DrissionPage import ChromiumPage
import concurrent.futures
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse, parse_qs

# HTTP请求头配置
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'referer': 'https://www.douyin.com/',
    'cookie': 'enter_pc_once=1; UIFID_TEMP=e71d819f1cb72e7166823ce125547a3e5a83b631a52f7c0b3c34cd9714dd602decd57fc863da49ac3d5c8057ba8a8de38516997b62f44d7150a428c8e29c90b59d3dc152c5ee33024c57f4fbe4378db8; hevc_supported=true; bd_ticket_guard_client_web_domain=2; d_ticket=acebe52cec47f168f7c670b5619cdfa723e61; passport_assist_user=CkDtTPu_80A6Ghm2zVspqB9lkoBaXPNHRYgqOx3_tb1eL_R1-7wNrbeYvfZCWF5SZt-XZYrWk_Kc_JC6ZviEakQxGkoKPAAAAAAAAAAAAABPJChkdGOJRmYlQxOChV2HdLumcTBww-kg4KXx4whMhaY6bfvMcUmRhPFqB_CZVG9Z8BCy1vQNGImv1lQgASIBA2n_ffY%3D; n_mh=JncE-KKZjDFZuD9j3PqEPSCSy2YYhNaTKQ4c7vZjUbg; uid_tt=7eaea83c7eb7e0b8d50a751e47817219; uid_tt_ss=7eaea83c7eb7e0b8d50a751e47817219; sid_tt=fa23d08f3750a8ef4f85b6d8d055796d; sessionid=fa23d08f3750a8ef4f85b6d8d055796d; sessionid_ss=fa23d08f3750a8ef4f85b6d8d055796d; is_staff_user=false; login_time=1750482446571'
}

def extract_collection_id(url):
    """从合集URL中提取合集ID"""
    try:
        path_parts = urlparse(url).path.split('/')
        if 'collection' in path_parts:
            collection_index = path_parts.index('collection')
            if collection_index + 1 < len(path_parts):
                collection_id = path_parts[collection_index + 1]
                print(f"✅ 提取到合集ID: {collection_id}")
                return collection_id
    except Exception as e:
        print(f"❌ 提取合集ID失败: {e}")
    return None

def create_download_directory(collection_id):
    """创建下载目录"""
    download_dir = f'downloads/collection_{collection_id}'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"📁 创建下载目录: {download_dir}")
    return download_dir

def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    illegal_chars = r'[<>:"/\\|?*]'
    safe_filename = re.sub(illegal_chars, '_', filename)
    if len(safe_filename) > 100:
        safe_filename = safe_filename[:100]
    return safe_filename

def download_video(video_url, filename, headers, max_retries=3):
    """下载视频文件"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    for attempt in range(max_retries + 1):
        try:
            print(f"📥 正在下载 {os.path.basename(filename)} (尝试 {attempt + 1}/{max_retries + 1})")
            
            with session.get(url=video_url, headers=headers, stream=True, timeout=(10, 60)) as r:
                r.raise_for_status()
                
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0 and downloaded % (1024 * 1024) == 0:
                                progress = (downloaded / total_size) * 100
                                print(f"  📊 进度: {progress:.1f}% ({downloaded//1024//1024}MB/{total_size//1024//1024}MB)")
                
                print(f"✅ 下载成功: {os.path.basename(filename)}")
                return True
                
        except requests.exceptions.Timeout:
            print(f"⏰ 下载超时 {os.path.basename(filename)} (尝试 {attempt + 1})")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求失败 {os.path.basename(filename)} (尝试 {attempt + 1}): {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"💥 意外错误 {os.path.basename(filename)}: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
    
    print(f"🚫 下载失败 {os.path.basename(filename)} - 已尝试 {max_retries + 1} 次")
    return False

def download_collection(collection_url, max_videos=100):
    """下载指定合集中的所有视频"""
    print(f"🎯 开始处理合集: {collection_url}")
    
    collection_id = extract_collection_id(collection_url)
    if not collection_id:
        print("❌ 无法提取合集ID，请检查URL格式")
        return
    
    download_dir = create_download_directory(collection_id)
    
    print("🌐 启动浏览器...")
    dp = ChromiumPage()
    
    try:
        # 监听所有可能的API路径
        print("🎧 开始监听网络请求...")
        dp.listen.start('aweme/v1/web/mix/aweme/')  # 合集API
        dp.listen.start('aweme/v1/web/aweme/post/')  # 用户视频API
        dp.listen.start('aweme/v1/web/general/search/single/')  # 搜索API
        dp.listen.start('aweme/v1/web/aweme/detail/')  # 详情API
        dp.listen.start('aweme/v1/web/aweme/related/')  # 相关视频API
        
        print(f"📖 正在访问合集页面...")
        dp.get(collection_url)
        
        print("⏳ 等待页面加载...")
        time.sleep(8)
        
        def smart_click_load_more():
            """智能点击加载更多按钮"""
            try:
                # 滚动到页面底部
                dp.scroll.to_bottom()
                time.sleep(2)
                
                # 尝试多种方式找到按钮
                button_selectors = [
                    'text:加载更多',
                    'text:点击获取更多视频',
                    'text:查看更多',
                    'text:展开更多',
                    'text:更多视频',
                    'text:Load More'
                ]
                
                for selector in button_selectors:
                    try:
                        elements = dp.eles(selector)
                        for element in elements:
                            try:
                                if element.states.is_displayed and element.states.is_enabled:
                                    element.click()
                                    print(f"✅ 成功点击按钮: {selector}")
                                    return True
                            except Exception:
                                continue
                    except Exception:
                        continue
                
                return False
            except Exception as e:
                print(f"❌ 点击按钮时出错: {e}")
                return False
        
        video_count = 0
        download_futures = []
        processed_ids = set()
        all_responses = []
        
        # 使用线程池进行并发下载
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            
            # 点击加载更多按钮并收集响应
            print("🔘 尝试加载所有视频...")
            for click_attempt in range(6):  # 按照您的要求，最多点击6次
                print(f"🔘 第 {click_attempt + 1} 次尝试点击加载更多...")
                
                if smart_click_load_more():
                    # 等待内容加载并收集API响应
                    time.sleep(4)  # 给更多时间让API响应
                    
                    # 收集这次点击产生的所有API响应
                    response_count = 0
                    while True:
                        try:
                            response = dp.listen.wait(timeout=2)
                            if response:
                                all_responses.append(response)
                                response_count += 1
                                print(f"📡 收集到API响应 #{len(all_responses)} (本次点击第{response_count}个)")
                            else:
                                break
                        except Exception:
                            break
                    
                    if response_count == 0:
                        print("⚠️ 本次点击没有产生新的API响应")
                else:
                    print(f"⚠️ 第 {click_attempt + 1} 次点击未成功，可能已加载完所有内容")
                    break
            
            print(f"📊 总共收集到 {len(all_responses)} 个API响应")
            
            # 处理所有收集到的API响应
            for i, response in enumerate(all_responses):
                try:
                    print(f"🔍 处理第 {i + 1} 个API响应...")
                    res_data = response.response.body
                    
                    # 打印API URL用于调试
                    api_url = response.url
                    print(f"🌐 API URL: {api_url}")
                    
                    # 查找视频列表
                    aweme_list = None
                    if 'aweme_list' in res_data:
                        aweme_list = res_data['aweme_list']
                        print(f"📋 在aweme_list中找到 {len(aweme_list)} 个视频")
                    elif 'data' in res_data and isinstance(res_data['data'], list):
                        aweme_list = res_data['data']
                        print(f"📋 在data中找到 {len(aweme_list)} 个视频")
                    elif 'aweme_info' in res_data:
                        aweme_list = [res_data['aweme_info']]
                        print(f"📋 在aweme_info中找到 1 个视频")
                    else:
                        print(f"⚠️ 响应中没有找到视频数据，响应键: {list(res_data.keys())}")
                        continue
                    
                    # 处理每个视频
                    for video_info in aweme_list:
                        if video_count >= max_videos:
                            break
                        
                        try:
                            aweme_id = video_info['aweme_id']
                            
                            if aweme_id in processed_ids:
                                continue
                            processed_ids.add(aweme_id)
                            
                            desc = video_info.get('desc', f'video_{aweme_id}')
                            video_url = video_info['video']['play_addr']['url_list'][0]
                            
                            print(f"🎬 [{video_count + 1}] {desc[:50]}...")
                            print(f"    🆔 ID: {aweme_id}")
                            
                            safe_desc = sanitize_filename(desc)
                            filename = os.path.join(download_dir, f'{aweme_id}_{safe_desc}.mp4')
                            
                            if os.path.exists(filename):
                                print(f"    ⏭️ 文件已存在，跳过下载")
                                video_count += 1  # 仍然计数，但不下载
                                continue
                            
                            future = executor.submit(download_video, video_url, filename, headers)
                            download_futures.append(future)
                            video_count += 1
                            
                        except KeyError as e:
                            print(f"⚠️ 视频信息缺失关键字段: {e}")
                            continue
                        except Exception as e:
                            print(f"❌ 处理视频信息时出错: {e}")
                            continue
                    
                    if video_count >= max_videos:
                        break
                        
                except Exception as e:
                    print(f"❌ 处理API响应时出错: {e}")
                    continue
            
            print(f"\n🎯 总共识别到 {video_count} 个视频")
            
            # 等待所有下载任务完成
            if download_futures:
                print(f"\n⏳ 开始下载 {len(download_futures)} 个视频...")
                successful_downloads = 0
                
                for i, future in enumerate(concurrent.futures.as_completed(download_futures), 1):
                    try:
                        result = future.result(timeout=300)
                        if result:
                            successful_downloads += 1
                        print(f"📊 总进度: {i}/{len(download_futures)} 完成")
                    except concurrent.futures.TimeoutError:
                        print(f"⏰ 下载任务超时")
                    except Exception as e:
                        print(f"❌ 下载任务异常: {e}")
                
                print(f"\n🎉 下载完成！成功: {successful_downloads}/{len(download_futures)}")
            else:
                print("⚠️ 没有找到需要下载的视频")
    
    except Exception as e:
        print(f"💥 程序执行过程中出现错误: {e}")
    
    finally:
        try:
            dp.quit()
            print("🔒 浏览器已关闭")
        except:
            pass
    
    # 显示下载结果统计
    if os.path.exists(download_dir):
        files = os.listdir(download_dir)
        print(f"\n📁 下载目录: {download_dir}")
        print(f"📊 文件数量: {len(files)} 个")
        
        for i, file in enumerate(files[:10], 1):
            print(f"  {i}. {file}")
        
        if len(files) > 10:
            print(f"  ... 还有 {len(files) - 10} 个文件")
    
    print(f"\n✨ 总共处理了 {video_count} 个视频")

def main():
    """主函数"""
    print("🚀 抖音合集下载器 - 最终版启动")
    print("=" * 50)
    
    collection_url = "https://www.douyin.com/collection/7446319576922458122/1?previous_page=others_homepage"
    
    if not collection_url:
        print("❌ 请提供有效的合集URL")
        return
    
    try:
        download_collection(collection_url, max_videos=100)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了程序执行")
    except Exception as e:
        print(f"💥 程序执行失败: {e}")
    
    print("\n👋 程序执行完毕")

if __name__ == "__main__":
    main()