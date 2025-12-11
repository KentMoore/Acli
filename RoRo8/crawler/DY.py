#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import re
from DrissionPage import ChromiumPage
import concurrent.futures
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'referer': 'https://www.douyin.com/',
    'cookie': 'enter_pc_once=1; UIFID_TEMP=e71d819f1cb72e7166823ce125547a3e5a83b631a52f7c0b3c34cd9714dd602decd57fc863da49ac3d5c8057ba8a8de38516997b62f44d7150a428c8e29c90b59d3dc152c5ee33024c57f4fbe4378db8; hevc_supported=true; bd_ticket_guard_client_web_domain=2; d_ticket=acebe52cec47f168f7c670b5619cdfa723e61; passport_assist_user=CkDtTPu_80A6Ghm2zVspqB9lkoBaXPNHRYgqOx3_tb1eL_R1-7wNrbeYvfZCWF5SZt-XZYrWk_Kc_JC6ZviEakQxGkoKPAAAAAAAAAAAAABPJChkdGOJRmYlQxOChV2HdLumcTBww-kg4KXx4whMhaY6bfvMcUmRhPFqB_CZVG9Z8BCy1vQNGImv1lQgASIBA2n_ffY%3D; n_mh=JncE-KKZjDFZuD9j3PqEPSCSy2YYhNaTKQ4c7vZjUbg; uid_tt=7eaea83c7eb7e0b8d50a751e47817219; uid_tt_ss=7eaea83c7eb7e0b8d50a751e47817219; sid_tt=fa23d08f3750a8ef4f85b6d8d055796d; sessionid=fa23d08f3750a8ef4f85b6d8d055796d; sessionid_ss=fa23d08f3750a8ef4f85b6d8d055796d; is_staff_user=false; login_time=1750482446571; UIFID=e71d819f1cb72e7166823ce125547a3e5a83b631a52f7c0b3c34cd9714dd602d834cb300b153814d43a3f2adfbcc56bbc225d0c598e8f5a885fed029678ff7d363ea9de08e430327892856093a0c28ee76cbd06df25f27f3caede7113101bc39065f7ce67619cdb2c79eb3df79b46d0e0cfd4e88714971c51c93350de571aed5fc5794529477d5f47194df7a1ef04511a227c636c8db0b4e29ed0711803e6dcf; _bd_ticket_crypt_cookie=d0b65fcae8d0dcaed4ae36bee32b73ab; SelfTabRedDotControl=%5B%5D; live_use_vvc=%22false%22; my_rd=2; SEARCH_RESULT_LIST_TYPE=%22single%22; is_dash_user=1; download_guide=%221%2F20250808%2F1%22; __live_version__=%221.1.3.6971%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A1%7D; passport_csrf_token=e91b4ccde722be73662b2ac6e298495a; passport_csrf_token_default=e91b4ccde722be73662b2ac6e298495a; __security_mc_1_s_sdk_crypt_sdk=d464cc90-4681-bc46; __security_mc_1_s_sdk_cert_key=59fa3bbb-4756-899d; __security_mc_1_s_sdk_sign_data_key_web_protect=4d5f95ec-4ed3-a0b0; h265ErrorNum=-1; publish_badge_show_info=%221%2C0%2C0%2C1756126793799%22; __druidClientInfo=JTdCJTIyY2xpZW50V2lkdGglMjIlM0EzMDQlMkMlMjJjbGllbnRIZWlnaHQlMjIlM0E2ODAlMkMlMjJ3aWR0aCUyMiUzQTMwNCUyQyUyMmhlaWdodCUyMiUzQTY4MCUyQyUyMmRldmljZVBpeGVsUmF0aW8lMjIlM0ExLjUlMkMlMjJ1c2VyQWdlbnQlMjIlM0ElMjJNb3ppbGxhJTJGNS4wJTIwKFdpbmRvd3MlMjBOVCUyMDEwLjAlM0IlMjBXaW42NCUzQiUyMHg2NCklMjBBcHBsZVdlYktpdCUyRjUzNy4zNiUyMChLSFRNTCUyQyUyMGxpa2UlMjBHZWNrbyklMjBDaHJvbWUlMkYxMzkuMC4wLjAlMjBTYWZhcmklMkY1MzcuMzYlMjIlN0Q=; strategyABtestKey=%221756693262.529%22; sid_guard=fa23d08f3750a8ef4f85b6d8d055796d%7C1756693268%7C5184000%7CFri%2C+31-Oct-2025+02%3A21%3A08+GMT; sid_ucp_v1=1.0.0-KDhiODAyYTYxMzU3YmZmMDc5NzUxMTRiNzllODNlNTk4MTI5OWU1MDEKIAiAtpDr1IwcEJSG1MUGGO8xIAwwhq3XggY4AkDxB0gEGgJscSIgZmEyM2QwOGYzNzUwYThlZjRmODViNmQ4ZDA1NTc5NmQ; ssid_ucp_v1=1.0.0-KDhiODAyYTYxMzU3YmZmMDc5NzUxMTRiNzllODNlNTk4MTI5OWU1MDEKIAiAtpDr1IwcEJSG1MUGGO8xIAwwhq3XggY4AkDxB0gEGgJscSIgZmEyM2QwOGYzNzUwYThlZjRmODViNmQ4ZDA1NTc5NmQ; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAD3REZFnZLHMqJ7UVytxdjLhNpTkeIs1gkQXWPyMvEKU%2F1756742400000%2F0%2F0%2F1756709069809%22; gulu_source_res=eyJwX2luIjoiZTBiNzA1NzgwZDUxMGU2MDhlNzEyM2YxMDgyMGE2YjEzOWU3OGMwMzkwY2NlMDQ2MDZlZWNmZjI5ZTBkNTJhYiJ9; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAD3REZFnZLHMqJ7UVytxdjLhNpTkeIs1gkQXWPyMvEKU%2F1756742400000%2F0%2F0%2F1756708559418%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1067%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A24%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; WallpaperGuide=%7B%22showTime%22%3A0%2C%22closeTime%22%3A1753842083083%2C%22showCount%22%3A0%2C%22cursor1%22%3A377%2C%22cursor2%22%3A263%2C%22hoverTime%22%3A1752321211383%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; playRecommendGuideTagCount=6; totalRecommendGuideTagCount=36; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e58272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f27303c343330363d353233303234272927676c715a75776a716a666a69273f2763646976602778; bit_env=7DQqMAbcuq8Z9HPXnOjlnkHHLCTvgVsm3SdU6syNf6IB3cnlgeETycLUWfsy9mAtiWEV0xJFKuSwEfs2_6sSyvUc8xNcJ71usV63lB5fgeqswFwNQ2nyTjqsOky-Umj0dGdn3GOtJHqG5_pRYVJ4RuFcQ2aaomHjjno8l3L0QErMxKCqDyPUcZDQZsJAT_DN1IOUapqot4hvpgphZsLTxQBNA6C0BJiiIe4H1tRaNA1lyVZKokXdA_lEO7uMnEwmbZNlsrml-EsJPzD3fjnuTGsxJ6FKjzd2gM1DqAwtZTvKXQLk5dNnt4c3qdRfSN9Kg8ycQzFXD02XmwvxSgM5ZCThgksUgIEqkusW8dXKItTHtkeS79ofEuq-sUsU8hul6GBEBIPMUaxyoPeAqfh4u9n9yUt8VvIoFotQifuYNexIYdg178Mg2R2KJYrKnGnpZVeBBCtzC1Q8ITHmLYU_QUvn_mCMGnePz7VEAADF5YWg32TKXb94sNwbHzjx5Veo; passport_auth_mix_state=6t763i6jorazn0cab7wjialrx1qo588ebqwtmju6d1ktshmq; biz_trace_id=e4681cb7; session_tlb_tag=sttt%7C11%7C-iPQjzdQqO9PhbbY0FV5bf_________PhgIqmnc-u2pcFB6SGKBoAev5iwkZGPYRFrj5zitgmhA%3D; IsDouyinActive=true; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQm1MMDh4TlQraVBpTGFKS0g2UUFrSVYvd2xvZTl1REdtdzdYenFlUUU0L1lCN3pRdGsva1RGU1p5N3crWjNNbUVxUFdDOXI0S1BLamptNit2WmdqQ2M9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; odin_tt=203512ecb33e498dc714aab019523e6e358ccd2c3c373a525d3ded46df58d08c1ff754024095edeb4ea575ec6c7d33df5e3a54349057ecb5580f693bac4b33b6778dafcbc69cf2c0fd7b1eac8a4c2436; ttwid=1%7CC2A0NeZbNDdoZDcKyEBKN61arf-AfLE_gTDoZDp8WLo%7C1756708539%7C06858e25fc26feae6c85af4aeef29ef1c0e6b25000d4ea5920c344221cee86f9'
}

# 确保下载目录存在
if not os.path.exists('downloads'):
    os.makedirs('downloads')

def download_video(video_url, filename, headers, max_retries=3):
    """Downloads a video from a URL and saves it to a file with retry mechanism."""
    session = requests.Session()
    
    # 配置重试策略
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
            print(f"Downloading {filename} (attempt {attempt + 1}/{max_retries + 1})")
            
            with session.get(url=video_url, headers=headers, stream=True, timeout=(10, 60)) as r:
                r.raise_for_status()
                
                # 获取文件大小
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 简单进度显示
                            if total_size > 0:
                                progress = (downloaded / total_size) * 100
                                if downloaded % (1024 * 1024) == 0:  # 每MB显示一次
                                    print(f"  Progress: {progress:.1f}% ({downloaded}/{total_size} bytes)")
                
                print(f"✅ Successfully downloaded: {filename}")
                return True
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout downloading {filename} (attempt {attempt + 1})")
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # 指数退避
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download {filename} (attempt {attempt + 1}): {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"💥 Unexpected error downloading {filename}: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
    
    print(f"🚫 Failed to download {filename} after {max_retries + 1} attempts")
    return False

dp = ChromiumPage()

dp.listen.start('aweme/v1/web/aweme/post/')
dp.get('https://www.douyin.com/user/MS4wLjABAAAA0p2KVQFjTJBJQXglI8tc6OOt4i9O-j9Bd7GMki9NWo8?from_tab_name=main&vid=7542844034759396646')
num = 0
download_futures = []  # 存储下载任务的future对象

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:  # 减少并发数避免网络拥堵
    for page in range(1, 20):
        start = dp.listen.wait()
        res = start.response.body

        for index in res['aweme_list']:
            aweme_id = index['aweme_id']
            desc = index['desc']
            video = index['video']['play_addr']['url_list'][0]
            print(f"[{num}] {desc[:50]}...")
            print(f"    URL: {video[:80]}...")
            num += 1
            
            # 清理文件名中的非法字符
            safe_desc = re.sub(r'[<>:"/\\|?*]', '_', desc)
            filename = f'downloads/{aweme_id}_{safe_desc[:50]}.mp4'  # 限制文件名长度

            # 提交下载任务并保存future对象
            future = executor.submit(download_video, video, filename, headers)
            download_futures.append(future)

        # 滚动加载更多内容
        try:
            dp.scroll.to_bottom()
            time.sleep(3)  # 等待页面加载
        except Exception as e:
            print(f"滚动失败: {e}")
    
    # 等待所有下载任务完成
    print(f"\n开始下载 {len(download_futures)} 个视频...")
    successful_downloads = 0
    
    for i, future in enumerate(concurrent.futures.as_completed(download_futures), 1):
        try:
            result = future.result()  # 获取下载结果
            if result:
                successful_downloads += 1
            print(f"进度: {i}/{len(download_futures)} 完成")
        except Exception as e:
            print(f"下载任务异常: {e}")
    
    print(f"\n下载完成！成功: {successful_downloads}/{len(download_futures)}")

# 最终检查downloads目录
if os.path.exists('downloads'):
    files = os.listdir('downloads')
    print(f"downloads目录中的文件: {len(files)} 个")
    for file in files[:5]:  # 显示前5个文件
        print(f"  - {file}")
else:
    print("downloads目录不存在")

print(f"\n总共处理了 {num} 个视频。")