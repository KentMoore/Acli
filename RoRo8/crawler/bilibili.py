import requests
import subprocess
import os
from tqdm import tqdm
import json
import uuid
import concurrent.futures
import threading

# Global lock for thread-safe printing with tqdm
tqdm.set_lock(threading.RLock())

# Bilibili video data (This will no longer be used directly for downloads)
video_data = {
    "video": [{
                          "id": 80,
                            "baseUrl": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100050.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&nbs=1&uipk=5&gen=playurlv3&os=bcache&og=hw&oi=2028943452&deadline=1751432217&upsig=68491d5f1edfea139120496057f038d5&uparams=e,mid,platform,trid,nbs,uipk,gen,os,og,oi,deadline&cdnid=10210&bvc=vod&nettype=0&bw=1455996&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=0,3",
                            "base_url": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100050.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&nbs=1&uipk=5&gen=playurlv3&os=bcache&og=hw&oi=2028943452&deadline=1751432217&upsig=68491d5f1edfea139120496057f038d5&uparams=e,mid,platform,trid,nbs,uipk,gen,os,og,oi,deadline&cdnid=10210&bvc=vod&nettype=0&bw=1455996&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=0,3",
                            "backupUrl": ["https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100050.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&uipk=5&os=08cbv&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&gen=playurlv3&og=hw&upsig=bcac08f40cea6f348c53bac0e6b52363&uparams=e,deadline,nbs,uipk,os,platform,trid,oi,mid,gen,og&bvc=vod&nettype=0&bw=1455996&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=1,3", "https://upos-sz-estghw.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100050.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&deadline=1751432217&nbs=1&os=upos&og=hw&mid=1393126795&upsig=9e62d22ed14e1ff14a172577e09124ee&uparams=e,uipk,platform,trid,oi,gen,deadline,nbs,os,og,mid&bvc=vod&nettype=0&bw=1455996&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=2,3"],
                            "backup_url": ["https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100050.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&uipk=5&os=08cbv&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&gen=playurlv3&og=hw&upsig=bcac08f40cea6f348c53bac0e6b52363&uparams=e,deadline,nbs,uipk,os,platform,trid,oi,mid,gen,og&bvc=vod&nettype=0&bw=1455996&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=1,3", "https://upos-sz-estghw.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100050.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&deadline=1751432217&nbs=1&os=upos&og=hw&mid=1393126795&upsig=9e62d22ed14e1ff14a172577e09124ee&uparams=e,uipk,platform,trid,oi,gen,deadline,nbs,os,og,mid&bvc=vod&nettype=0&bw=1455996&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=2,3"],
                            "bandwidth": 1455975,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "avc1.640032",
                            "width": 1920,
                            "height": 1080,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-940",
                                "indexRange": "941-9000"
                            },
                            "segment_base": {
                                "initialization": "0-940",
                                "index_range": "941-9000"
                            },
                            "codecid": 7
                        }, {
                            "id": 80,
                            "baseUrl": "https://xy183x232x204x8xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30077.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=1643090&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=9291cc&traceid=trHgLuthPkntYZ_0_e_N&uipk=5&uparams=e%2Cmid%2Cuipk%2Cplatform%2Cgen%2Cog%2Coi%2Cdeadline%2Cnbs%2Ctrid%2Cos&upsig=03a5e811a5cb4bcc3d39ba0756905827",
                            "base_url": "https://xy183x232x204x8xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30077.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=1643090&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=9291cc&traceid=trHgLuthPkntYZ_0_e_N&uipk=5&uparams=e%2Cmid%2Cuipk%2Cplatform%2Cgen%2Cog%2Coi%2Cdeadline%2Cnbs%2Ctrid%2Cos&upsig=03a5e811a5cb4bcc3d39ba0756905827",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30077.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&uipk=5&platform=pc&gen=playurlv3&og=hw&oi=2028943452&deadline=1751432217&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&os=bcache&upsig=03a5e811a5cb4bcc3d39ba0756905827&uparams=e,mid,uipk,platform,gen,og,oi,deadline,nbs,trid,os&cdnid=10210&bvc=vod&nettype=0&bw=1643090&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30077.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&platform=pc&gen=playurlv3&os=08cbv&og=hw&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&upsig=1cac51f3ba65799528fa9a183c600185&uparams=e,deadline,nbs,platform,gen,os,og,uipk,trid,oi,mid&bvc=vod&nettype=0&bw=1643090&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30077.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&uipk=5&platform=pc&gen=playurlv3&og=hw&oi=2028943452&deadline=1751432217&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&os=bcache&upsig=03a5e811a5cb4bcc3d39ba0756905827&uparams=e,mid,uipk,platform,gen,og,oi,deadline,nbs,trid,os&cdnid=10210&bvc=vod&nettype=0&bw=1643090&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30077.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&platform=pc&gen=playurlv3&os=08cbv&og=hw&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&upsig=1cac51f3ba65799528fa9a183c600185&uparams=e,deadline,nbs,platform,gen,os,og,uipk,trid,oi,mid&bvc=vod&nettype=0&bw=1643090&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "bandwidth": 1643069,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "hev1.1.6.L150.90",
                            "width": 1920,
                            "height": 1080,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1004",
                                "indexRange": "1005-9064"
                            },
                            "segment_base": {
                                "initialization": "0-1004",
                                "index_range": "1005-9064"
                            },
                            "codecid": 12
                        }, {
                            "id": 80,
                            "baseUrl": "https://xy120x240x155x137xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100026.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=1458827&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=f3ab2f&traceid=trKJNKnifAIjSy_0_e_N&uipk=5&uparams=e%2Cog%2Cmid%2Cnbs%2Coi%2Ctrid%2Cgen%2Cos%2Cdeadline%2Cuipk%2Cplatform&upsig=5bb1a458ca01a95f8c3f3a58360ffbb5",
                            "base_url": "https://xy120x240x155x137xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100026.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=1458827&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=f3ab2f&traceid=trKJNKnifAIjSy_0_e_N&uipk=5&uparams=e%2Cog%2Cmid%2Cnbs%2Coi%2Ctrid%2Cgen%2Cos%2Cdeadline%2Cuipk%2Cplatform&upsig=5bb1a458ca01a95f8c3f3a58360ffbb5",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100026.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&og=hw&mid=1393126795&nbs=1&oi=2028943452&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&os=bcache&deadline=1751432217&uipk=5&platform=pc&upsig=5bb1a458ca01a95f8c3f3a58360ffbb5&uparams=e,og,mid,nbs,oi,trid,gen,os,deadline,uipk,platform&cdnid=10210&bvc=vod&nettype=0&bw=1458827&build=0&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100026.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&nbs=1&gen=playurlv3&os=08cbv&mid=1393126795&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&og=hw&deadline=1751432217&upsig=a1e3eff909cd465eaccfc0f4a6c218d7&uparams=e,nbs,gen,os,mid,uipk,platform,trid,oi,og,deadline&bvc=vod&nettype=0&bw=1458827&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100026.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&og=hw&mid=1393126795&nbs=1&oi=2028943452&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&os=bcache&deadline=1751432217&uipk=5&platform=pc&upsig=5bb1a458ca01a95f8c3f3a58360ffbb5&uparams=e,og,mid,nbs,oi,trid,gen,os,deadline,uipk,platform&cdnid=10210&bvc=vod&nettype=0&bw=1458827&build=0&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100026.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&nbs=1&gen=playurlv3&os=08cbv&mid=1393126795&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&og=hw&deadline=1751432217&upsig=a1e3eff909cd465eaccfc0f4a6c218d7&uparams=e,nbs,gen,os,mid,uipk,platform,trid,oi,og,deadline&bvc=vod&nettype=0&bw=1458827&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "bandwidth": 1458805,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "av01.0.00M.10.0.110.01.01.01.0",
                            "width": 1920,
                            "height": 1080,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1006",
                                "indexRange": "1007-9066"
                            },
                            "segment_base": {
                                "initialization": "0-1006",
                                "index_range": "1007-9066"
                            },
                            "codecid": 13
                        }, {
                            "id": 64,
                            "baseUrl": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100048.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&og=cos&deadline=1751432217&uipk=5&platform=pc&gen=playurlv3&os=bcache&upsig=bf9f0f56a7fe804268efb05b795395db&uparams=e,mid,nbs,trid,oi,og,deadline,uipk,platform,gen,os&cdnid=10210&bvc=vod&nettype=0&bw=833454&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=0,3",
                            "base_url": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100048.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&og=cos&deadline=1751432217&uipk=5&platform=pc&gen=playurlv3&os=bcache&upsig=bf9f0f56a7fe804268efb05b795395db&uparams=e,mid,nbs,trid,oi,og,deadline,uipk,platform,gen,os&cdnid=10210&bvc=vod&nettype=0&bw=833454&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=0,3",
                            "backupUrl": ["https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100048.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&gen=playurlv3&os=upos&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&platform=pc&og=cos&mid=1393126795&deadline=1751432217&nbs=1&upsig=49bcfeb9acb01b46c70cf2a98739bba2&uparams=e,gen,os,uipk,trid,oi,platform,og,mid,deadline,nbs&bvc=vod&nettype=0&bw=833454&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3", "https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100048.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&oi=2028943452&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&os=cosbv&og=cos&mid=1393126795&uipk=5&platform=pc&upsig=1becf118ee68532cc014bef093b6af65&uparams=e,deadline,nbs,oi,trid,gen,os,og,mid,uipk,platform&bvc=vod&nettype=0&bw=833454&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=2,3"],
                            "backup_url": ["https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100048.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&gen=playurlv3&os=upos&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&platform=pc&og=cos&mid=1393126795&deadline=1751432217&nbs=1&upsig=49bcfeb9acb01b46c70cf2a98739bba2&uparams=e,gen,os,uipk,trid,oi,platform,og,mid,deadline,nbs&bvc=vod&nettype=0&bw=833454&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3", "https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100048.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&oi=2028943452&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&os=cosbv&og=cos&mid=1393126795&uipk=5&platform=pc&upsig=1becf118ee68532cc014bef093b6af65&uparams=e,deadline,nbs,oi,trid,gen,os,og,mid,uipk,platform&bvc=vod&nettype=0&bw=833454&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=2,3"],
                            "bandwidth": 833433,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "avc1.640028",
                            "width": 1280,
                            "height": 720,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-940",
                                "indexRange": "941-9000"
                            },
                            "segment_base": {
                                "initialization": "0-940",
                                "index_range": "941-9000"
                            },
                            "codecid": 7
                        }, {
                            "id": 64,
                            "baseUrl": "https://xy183x232x204x18xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30066.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=623084&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=9721e4&traceid=trWyAcdabHTKUO_0_e_N&uipk=5&uparams=e%2Cmid%2Cdeadline%2Cnbs%2Cplatform%2Cog%2Ctrid%2Coi%2Cuipk%2Cgen%2Cos&upsig=58765d7a71b61de2fc2a4d0d5f444941",
                            "base_url": "https://xy183x232x204x18xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30066.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=623084&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=9721e4&traceid=trWyAcdabHTKUO_0_e_N&uipk=5&uparams=e%2Cmid%2Cdeadline%2Cnbs%2Cplatform%2Cog%2Ctrid%2Coi%2Cuipk%2Cgen%2Cos&upsig=58765d7a71b61de2fc2a4d0d5f444941",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30066.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&deadline=1751432217&nbs=1&platform=pc&og=hw&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&uipk=5&gen=playurlv3&os=bcache&upsig=58765d7a71b61de2fc2a4d0d5f444941&uparams=e,mid,deadline,nbs,platform,og,trid,oi,uipk,gen,os&cdnid=10210&bvc=vod&nettype=0&bw=623084&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30066.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&og=hw&os=08cbv&mid=1393126795&deadline=1751432217&nbs=1&uipk=5&oi=2028943452&upsig=60bb756b3ec5efcf13b9aaa19da8d3a7&uparams=e,platform,trid,gen,og,os,mid,deadline,nbs,uipk,oi&bvc=vod&nettype=0&bw=623084&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30066.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&deadline=1751432217&nbs=1&platform=pc&og=hw&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&uipk=5&gen=playurlv3&os=bcache&upsig=58765d7a71b61de2fc2a4d0d5f444941&uparams=e,mid,deadline,nbs,platform,og,trid,oi,uipk,gen,os&cdnid=10210&bvc=vod&nettype=0&bw=623084&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30066.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&og=hw&os=08cbv&mid=1393126795&deadline=1751432217&nbs=1&uipk=5&oi=2028943452&upsig=60bb756b3ec5efcf13b9aaa19da8d3a7&uparams=e,platform,trid,gen,og,os,mid,deadline,nbs,uipk,oi&bvc=vod&nettype=0&bw=623084&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=1,3"],
                            "bandwidth": 623063,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "hev1.1.6.L120.90",
                            "width": 1280,
                            "height": 720,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1003",
                                "indexRange": "1004-9063"
                            },
                            "segment_base": {
                                "initialization": "0-1003",
                                "index_range": "1004-9063"
                            },
                            "codecid": 12
                        }, {
                            "id": 64,
                            "baseUrl": "https://xy183x240x59x133xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100024.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=545458&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=aed24c&traceid=trCuKqdtnARRgo_0_e_N&uipk=5&uparams=e%2Cmid%2Cos%2Cog%2Ctrid%2Coi%2Cdeadline%2Cnbs%2Cuipk%2Cgen%2Cplatform&upsig=9acc69fe63848605e97a2f6a4f79ad73",
                            "base_url": "https://xy183x240x59x133xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100024.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=545458&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=aed24c&traceid=trCuKqdtnARRgo_0_e_N&uipk=5&uparams=e%2Cmid%2Cos%2Cog%2Ctrid%2Coi%2Cdeadline%2Cnbs%2Cuipk%2Cgen%2Cplatform&upsig=9acc69fe63848605e97a2f6a4f79ad73",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100024.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&os=bcache&og=cos&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&deadline=1751432217&nbs=1&uipk=5&gen=playurlv3&platform=pc&upsig=9acc69fe63848605e97a2f6a4f79ad73&uparams=e,mid,os,og,trid,oi,deadline,nbs,uipk,gen,platform&cdnid=10210&bvc=vod&nettype=0&bw=545458&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgoss.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100024.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=upos&og=cos&oi=2028943452&nbs=1&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&mid=1393126795&deadline=1751432217&uipk=5&upsig=01794ca221b383afd1eb2e2883786df2&uparams=e,os,og,oi,nbs,platform,trid,gen,mid,deadline,uipk&bvc=vod&nettype=0&bw=545458&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100024.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&os=bcache&og=cos&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&deadline=1751432217&nbs=1&uipk=5&gen=playurlv3&platform=pc&upsig=9acc69fe63848605e97a2f6a4f79ad73&uparams=e,mid,os,og,trid,oi,deadline,nbs,uipk,gen,platform&cdnid=10210&bvc=vod&nettype=0&bw=545458&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgoss.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100024.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=upos&og=cos&oi=2028943452&nbs=1&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&mid=1393126795&deadline=1751432217&uipk=5&upsig=01794ca221b383afd1eb2e2883786df2&uparams=e,os,og,oi,nbs,platform,trid,gen,mid,deadline,uipk&bvc=vod&nettype=0&bw=545458&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "bandwidth": 545436,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "av01.0.00M.10.0.110.01.01.01.0",
                            "width": 1280,
                            "height": 720,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1006",
                                "indexRange": "1007-9066"
                            },
                            "segment_base": {
                                "initialization": "0-1006",
                                "index_range": "1007-9066"
                            },
                            "codecid": 13
                        }, {
                            "id": 32,
                            "baseUrl": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100047.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&gen=playurlv3&os=bcache&mid=1393126795&nbs=1&oi=2028943452&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&og=hw&deadline=1751432217&uipk=5&platform=pc&upsig=dc169de5ed35c5d79008b9c398576798&uparams=e,gen,os,mid,nbs,oi,trid,og,deadline,uipk,platform&cdnid=10210&bvc=vod&nettype=0&bw=420236&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3",
                            "base_url": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100047.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&gen=playurlv3&os=bcache&mid=1393126795&nbs=1&oi=2028943452&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&og=hw&deadline=1751432217&uipk=5&platform=pc&upsig=dc169de5ed35c5d79008b9c398576798&uparams=e,gen,os,mid,nbs,oi,trid,og,deadline,uipk,platform&cdnid=10210&bvc=vod&nettype=0&bw=420236&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3",
                            "backupUrl": ["https://upos-sz-estghw.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100047.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&oi=2028943452&mid=1393126795&deadline=1751432217&nbs=1&gen=playurlv3&og=hw&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&os=upos&upsig=8c43fcfd2c3f4af13d6da252495943ca&uparams=e,platform,oi,mid,deadline,nbs,gen,og,uipk,trid,os&bvc=vod&nettype=0&bw=420236&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100047.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&oi=2028943452&mid=1393126795&os=08cbv&og=hw&nbs=1&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&upsig=820b651baf61dbab5f6346e76beacc7d&uparams=e,deadline,oi,mid,os,og,nbs,uipk,platform,trid,gen&bvc=vod&nettype=0&bw=420236&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=2,3"],
                            "backup_url": ["https://upos-sz-estghw.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100047.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&oi=2028943452&mid=1393126795&deadline=1751432217&nbs=1&gen=playurlv3&og=hw&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&os=upos&upsig=8c43fcfd2c3f4af13d6da252495943ca&uparams=e,platform,oi,mid,deadline,nbs,gen,og,uipk,trid,os&bvc=vod&nettype=0&bw=420236&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100047.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&oi=2028943452&mid=1393126795&os=08cbv&og=hw&nbs=1&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&upsig=820b651baf61dbab5f6346e76beacc7d&uparams=e,deadline,oi,mid,os,og,nbs,uipk,platform,trid,gen&bvc=vod&nettype=0&bw=420236&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=2,3"],
                            "bandwidth": 420215,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "avc1.64001F",
                            "width": 852,
                            "height": 480,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-939",
                                "indexRange": "940-8999"
                            },
                            "segment_base": {
                                "initialization": "0-939",
                                "index_range": "940-8999"
                            },
                            "codecid": 7
                        }, {
                            "id": 32,
                            "baseUrl": "https://xy118x184x254x78xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30033.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=297551&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=6c90aa&traceid=trmXJtMZerVUOd_0_e_N&uipk=5&uparams=e%2Ctrid%2Coi%2Cgen%2Cos%2Cmid%2Cnbs%2Cplatform%2Cdeadline%2Cuipk%2Cog&upsig=c2f08a488d1abbd9cbb5470e610b0d12",
                            "base_url": "https://xy118x184x254x78xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30033.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=297551&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=6c90aa&traceid=trmXJtMZerVUOd_0_e_N&uipk=5&uparams=e%2Ctrid%2Coi%2Cgen%2Cos%2Cmid%2Cnbs%2Cplatform%2Cdeadline%2Cuipk%2Cog&upsig=c2f08a488d1abbd9cbb5470e610b0d12",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30033.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&os=bcache&mid=1393126795&nbs=1&platform=pc&deadline=1751432217&uipk=5&og=hw&upsig=c2f08a488d1abbd9cbb5470e610b0d12&uparams=e,trid,oi,gen,os,mid,nbs,platform,deadline,uipk,og&cdnid=10210&bvc=vod&nettype=0&bw=297551&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estghw.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30033.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&platform=pc&oi=2028943452&nbs=1&gen=playurlv3&os=upos&og=hw&upsig=59c5e0a6b0e9398bff4a4077d6993465&uparams=e,uipk,trid,mid,deadline,platform,oi,nbs,gen,os,og&bvc=vod&nettype=0&bw=297551&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30033.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&os=bcache&mid=1393126795&nbs=1&platform=pc&deadline=1751432217&uipk=5&og=hw&upsig=c2f08a488d1abbd9cbb5470e610b0d12&uparams=e,trid,oi,gen,os,mid,nbs,platform,deadline,uipk,og&cdnid=10210&bvc=vod&nettype=0&bw=297551&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estghw.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30033.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&platform=pc&oi=2028943452&nbs=1&gen=playurlv3&os=upos&og=hw&upsig=59c5e0a6b0e9398bff4a4077d6993465&uparams=e,uipk,trid,mid,deadline,platform,oi,nbs,gen,os,og&bvc=vod&nettype=0&bw=297551&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "bandwidth": 297530,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "hev1.1.6.L120.90",
                            "width": 852,
                            "height": 480,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1004",
                                "indexRange": "1005-9064"
                            },
                            "segment_base": {
                                "initialization": "0-1004",
                                "index_range": "1005-9064"
                            },
                            "codecid": 12
                        }, {
                            "id": 32,
                            "baseUrl": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&og=hw&mid=1393126795&uipk=5&os=bcache&upsig=adaa72bf25e6e95373ab70bcd9831511&uparams=e,deadline,nbs,platform,trid,oi,gen,og,mid,uipk,os&cdnid=10210&bvc=vod&nettype=0&bw=257777&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3",
                            "base_url": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1751432217&nbs=1&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&og=hw&mid=1393126795&uipk=5&os=bcache&upsig=adaa72bf25e6e95373ab70bcd9831511&uparams=e,deadline,nbs,platform,trid,oi,gen,og,mid,uipk,os&cdnid=10210&bvc=vod&nettype=0&bw=257777&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3",
                            "backupUrl": ["https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&nbs=1&uipk=5&oi=2028943452&gen=playurlv3&os=bdbv&og=hw&upsig=5bdc4243b28443118a8c3e1941e78216&uparams=e,platform,trid,mid,deadline,nbs,uipk,oi,gen,os,og&bvc=vod&nettype=0&bw=257777&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3", "https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&nbs=1&uipk=5&oi=2028943452&gen=playurlv3&os=bdbv&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&og=hw&upsig=0ef8091d1bd7e3e882e48b9414ca2e69&uparams=e,nbs,uipk,oi,gen,os,platform,trid,mid,deadline,og&bvc=vod&nettype=0&bw=257777&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=2,3"],
                            "backup_url": ["https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&nbs=1&uipk=5&oi=2028943452&gen=playurlv3&os=bdbv&og=hw&upsig=5bdc4243b28443118a8c3e1941e78216&uparams=e,platform,trid,mid,deadline,nbs,uipk,oi,gen,os,og&bvc=vod&nettype=0&bw=257777&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3", "https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100023.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&nbs=1&uipk=5&oi=2028943452&gen=playurlv3&os=bdbv&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&og=hw&upsig=0ef8091d1bd7e3e882e48b9414ca2e69&uparams=e,nbs,uipk,oi,gen,os,platform,trid,mid,deadline,og&bvc=vod&nettype=0&bw=257777&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=2,3"],
                            "bandwidth": 257756,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "av01.0.00M.10.0.110.01.01.01.0",
                            "width": 852,
                            "height": 480,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1006",
                                "indexRange": "1007-9066"
                            },
                            "segment_base": {
                                "initialization": "0-1006",
                                "index_range": "1007-9066"
                            },
                            "codecid": 13
                        }, {
                            "id": 16,
                            "baseUrl": "https://xy183x238x66x26xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100046.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=239015&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=225921&traceid=trfGiKQcqroPDn_0_e_N&uipk=5&uparams=e%2Cos%2Cuipk%2Cplatform%2Ctrid%2Cgen%2Cog%2Coi%2Cmid%2Cdeadline%2Cnbs&upsig=c4857f425a185dc425527b750604adbb",
                            "base_url": "https://xy183x238x66x26xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100046.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=239015&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=225921&traceid=trfGiKQcqroPDn_0_e_N&uipk=5&uparams=e%2Cos%2Cuipk%2Cplatform%2Ctrid%2Cgen%2Cog%2Coi%2Cmid%2Cdeadline%2Cnbs&upsig=c4857f425a185dc425527b750604adbb",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100046.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=bcache&uipk=5&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&og=cos&oi=2028943452&mid=1393126795&deadline=1751432217&nbs=1&upsig=c4857f425a185dc425527b750604adbb&uparams=e,os,uipk,platform,trid,gen,og,oi,mid,deadline,nbs&cdnid=10210&bvc=vod&nettype=0&bw=239015&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100046.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&deadline=1751432217&uipk=5&gen=playurlv3&og=cos&platform=pc&nbs=1&os=upos&upsig=55b1398e5b9969f06bd67ae82a1fc3b2&uparams=e,trid,oi,mid,deadline,uipk,gen,og,platform,nbs,os&bvc=vod&nettype=0&bw=239015&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100046.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=bcache&uipk=5&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&og=cos&oi=2028943452&mid=1393126795&deadline=1751432217&nbs=1&upsig=c4857f425a185dc425527b750604adbb&uparams=e,os,uipk,platform,trid,gen,og,oi,mid,deadline,nbs&cdnid=10210&bvc=vod&nettype=0&bw=239015&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100046.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&deadline=1751432217&uipk=5&gen=playurlv3&og=cos&platform=pc&nbs=1&os=upos&upsig=55b1398e5b9969f06bd67ae82a1fc3b2&uparams=e,trid,oi,mid,deadline,uipk,gen,og,platform,nbs,os&bvc=vod&nettype=0&bw=239015&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "bandwidth": 238994,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "avc1.64001E",
                            "width": 640,
                            "height": 360,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-946",
                                "indexRange": "947-9006"
                            },
                            "segment_base": {
                                "initialization": "0-946",
                                "index_range": "947-9006"
                            },
                            "codecid": 7
                        }, {
                            "id": 16,
                            "baseUrl": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30011.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&deadline=1751432217&nbs=1&uipk=5&og=cos&mid=1393126795&gen=playurlv3&os=bcache&upsig=19326e4ad51d10d3fea0e54355d1d3d7&uparams=e,platform,trid,oi,deadline,nbs,uipk,og,mid,gen,os&cdnid=10210&bvc=vod&nettype=0&bw=198454&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=0,3",
                            "base_url": "https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30011.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&platform=pc&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&deadline=1751432217&nbs=1&uipk=5&og=cos&mid=1393126795&gen=playurlv3&os=bcache&upsig=19326e4ad51d10d3fea0e54355d1d3d7&uparams=e,platform,trid,oi,deadline,nbs,uipk,og,mid,gen,os&cdnid=10210&bvc=vod&nettype=0&bw=198454&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=0,3",
                            "backupUrl": ["https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30011.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=upos&nbs=1&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&gen=playurlv3&deadline=1751432217&og=cos&upsig=41374c2c8085dc3ab558fd11229c9ffa&uparams=e,os,nbs,uipk,platform,trid,oi,mid,gen,deadline,og&bvc=vod&nettype=0&bw=198454&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=1,3", "https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30011.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&nbs=1&gen=playurlv3&deadline=1751432217&os=cosbv&og=cos&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&upsig=2fa68cc2ca849b0c07db79277c7294e9&uparams=e,mid,nbs,gen,deadline,os,og,uipk,platform,trid,oi&bvc=vod&nettype=0&bw=198454&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=2,3"],
                            "backup_url": ["https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30011.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=upos&nbs=1&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&mid=1393126795&gen=playurlv3&deadline=1751432217&og=cos&upsig=41374c2c8085dc3ab558fd11229c9ffa&uparams=e,os,nbs,uipk,platform,trid,oi,mid,gen,deadline,og&bvc=vod&nettype=0&bw=198454&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=1,3", "https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30011.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&nbs=1&gen=playurlv3&deadline=1751432217&os=cosbv&og=cos&uipk=5&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&upsig=2fa68cc2ca849b0c07db79277c7294e9&uparams=e,mid,nbs,gen,deadline,os,og,uipk,platform,trid,oi&bvc=vod&nettype=0&bw=198454&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=2,3"],
                            "bandwidth": 198433,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "hev1.1.6.L120.90",
                            "width": 640,
                            "height": 360,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1004",
                                "indexRange": "1005-9064"
                            },
                            "segment_base": {
                                "initialization": "0-1004",
                                "index_range": "1005-9064"
                            },
                            "codecid": 12
                        }, {
                            "id": 16,
                            "baseUrl": "https://xy182x89x195x75xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100022.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=176470&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=bb0bad&traceid=trGZgIdUfjiHgJ_0_e_N&uipk=5&uparams=e%2Cos%2Cog%2Cplatform%2Coi%2Cnbs%2Cgen%2Ctrid%2Cmid%2Cdeadline%2Cuipk&upsig=10ec5c5abb99aadcd6fe122334ea66a2",
                            "base_url": "https://xy182x89x195x75xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-100022.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=176470&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=bb0bad&traceid=trGZgIdUfjiHgJ_0_e_N&uipk=5&uparams=e%2Cos%2Cog%2Cplatform%2Coi%2Cnbs%2Cgen%2Ctrid%2Cmid%2Cdeadline%2Cuipk&upsig=10ec5c5abb99aadcd6fe122334ea66a2",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100022.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=bcache&og=hw&platform=pc&oi=2028943452&nbs=1&gen=playurlv3&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&uipk=5&upsig=10ec5c5abb99aadcd6fe122334ea66a2&uparams=e,os,og,platform,oi,nbs,gen,trid,mid,deadline,uipk&cdnid=10210&bvc=vod&nettype=0&bw=176470&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=0,3", "https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100022.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=e9fc696ac5494436a3d8187ebbf80a6u&deadline=1751432217&uipk=5&gen=playurlv3&os=bdbv&oi=2028943452&mid=1393126795&nbs=1&platform=pc&og=hw&upsig=970c107d3ba0eff88e59453cc5e01cb9&uparams=e,trid,deadline,uipk,gen,os,oi,mid,nbs,platform,og&bvc=vod&nettype=0&bw=176470&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100022.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=bcache&og=hw&platform=pc&oi=2028943452&nbs=1&gen=playurlv3&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&uipk=5&upsig=10ec5c5abb99aadcd6fe122334ea66a2&uparams=e,os,og,platform,oi,nbs,gen,trid,mid,deadline,uipk&cdnid=10210&bvc=vod&nettype=0&bw=176470&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=0,3", "https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-100022.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=e9fc696ac5494436a3d8187ebbf80a6u&deadline=1751432217&uipk=5&gen=playurlv3&os=bdbv&oi=2028943452&mid=1393126795&nbs=1&platform=pc&og=hw&upsig=970c107d3ba0eff88e59453cc5e01cb9&uparams=e,trid,deadline,uipk,gen,os,oi,mid,nbs,platform,og&bvc=vod&nettype=0&bw=176470&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=1,3"],
                            "bandwidth": 176448,
                            "mimeType": "video/mp4",
                            "mime_type": "video/mp4",
                            "codecs": "av01.0.00M.10.0.110.01.01.01.0",
                            "width": 640,
                            "height": 360,
                            "frameRate": "30.000",
                            "frame_rate": "30.000",
                            "sar": "N/A",
                            "startWithSap": 1,
                            "start_with_sap": 1,
                            "SegmentBase": {
                                "Initialization": "0-1006",
                                "indexRange": "1007-9066"
                            },
                            "segment_base": {
                                "initialization": "0-1006",
                                "index_range": "1007-9066"
                            },
                            "codecid": 13
                        }],
 "audio": [{
                           "id": 30232,
                            "baseUrl": "https://xy183x240x59x187xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30232.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=323291&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=d41e2f&traceid=truRuKERCjVBdD_0_e_N&uipk=5&uparams=e%2Cos%2Cog%2Cnbs%2Ctrid%2Cgen%2Cplatform%2Coi%2Cmid%2Cdeadline%2Cuipk&upsig=d385c53e03293fecbef994f88a6e297d",
                            "base_url": "https://xy183x240x59x187xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30232.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=323291&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=d41e2f&traceid=truRuKERCjVBdD_0_e_N&uipk=5&uparams=e%2Cos%2Cog%2Cnbs%2Ctrid%2Cgen%2Cplatform%2Coi%2Cmid%2Cdeadline%2Cuipk&upsig=d385c53e03293fecbef994f88a6e297d",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=bcache&og=cos&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&platform=pc&oi=2028943452&mid=1393126795&deadline=1751432217&uipk=5&upsig=d385c53e03293fecbef994f88a6e297d&uparams=e,os,og,nbs,trid,gen,platform,oi,mid,deadline,uipk&cdnid=10210&bvc=vod&nettype=0&bw=323291&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&deadline=1751432217&platform=pc&og=cos&nbs=1&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&os=upos&upsig=167de8e9e62d51b71ada9293d4e40eb3&uparams=e,mid,deadline,platform,og,nbs,uipk,trid,oi,gen,os&bvc=vod&nettype=0&bw=323291&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&os=bcache&og=cos&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&platform=pc&oi=2028943452&mid=1393126795&deadline=1751432217&uipk=5&upsig=d385c53e03293fecbef994f88a6e297d&uparams=e,os,og,nbs,trid,gen,platform,oi,mid,deadline,uipk&cdnid=10210&bvc=vod&nettype=0&bw=323291&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&mid=1393126795&deadline=1751432217&platform=pc&og=cos&nbs=1&uipk=5&trid=e9fc696ac5494436a3d8187ebbf80a6u&oi=2028943452&gen=playurlv3&os=upos&upsig=167de8e9e62d51b71ada9293d4e40eb3&uparams=e,mid,deadline,platform,og,nbs,uipk,trid,oi,gen,os&bvc=vod&nettype=0&bw=323291&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&agrr=0&orderid=1,3"],
                            "bandwidth": 323175,
                            "mimeType": "audio/mp4",
                            "mime_type": "audio/mp4",
                            "codecs": "mp4a.40.2",
                            "width": 0,
                            "height": 0,
                            "frameRate": "",
                            "frame_rate": "",
                            "sar": "",
                            "startWithSap": 0,
                            "start_with_sap": 0,
                            "SegmentBase": {
                                "Initialization": "0-781",
                                "indexRange": "782-8837"
                            },
                            "segment_base": {
                                "initialization": "0-781",
                                "index_range": "782-8837"
                            },
                            "codecid": 0
                        }, {
                            "id": 30216,
                            "baseUrl": "https://xy183x232x204x8xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30216.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=323291&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=014143&traceid=trORRbMoLrUgWo_0_e_N&uipk=5&uparams=e%2Coi%2Cmid%2Cdeadline%2Cnbs%2Ctrid%2Cgen%2Cog%2Cuipk%2Cplatform%2Cos&upsig=171435ae74f631eccf080d1fdc9a6108",
                            "base_url": "https://xy183x232x204x8xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30216.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=323291&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=cos&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=014143&traceid=trORRbMoLrUgWo_0_e_N&uipk=5&uparams=e%2Coi%2Cmid%2Cdeadline%2Cnbs%2Ctrid%2Cgen%2Cog%2Cuipk%2Cplatform%2Cos&upsig=171435ae74f631eccf080d1fdc9a6108",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=2028943452&mid=1393126795&deadline=1751432217&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&og=cos&uipk=5&platform=pc&os=bcache&upsig=171435ae74f631eccf080d1fdc9a6108&uparams=e,oi,mid,deadline,nbs,trid,gen,og,uipk,platform,os&cdnid=10210&bvc=vod&nettype=0&bw=323291&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&uipk=5&platform=pc&os=upos&oi=2028943452&nbs=1&gen=playurlv3&og=cos&upsig=83674984e91f0655a67c882c6d2a7eb2&uparams=e,trid,mid,deadline,uipk,platform,os,oi,nbs,gen,og&bvc=vod&nettype=0&bw=323291&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=2028943452&mid=1393126795&deadline=1751432217&nbs=1&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&gen=playurlv3&og=cos&uipk=5&platform=pc&os=bcache&upsig=171435ae74f631eccf080d1fdc9a6108&uparams=e,oi,mid,deadline,nbs,trid,gen,og,uipk,platform,os&cdnid=10210&bvc=vod&nettype=0&bw=323291&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=0,3", "https://upos-sz-estgcos.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&deadline=1751432217&uipk=5&platform=pc&os=upos&oi=2028943452&nbs=1&gen=playurlv3&og=cos&upsig=83674984e91f0655a67c882c6d2a7eb2&uparams=e,trid,mid,deadline,uipk,platform,os,oi,nbs,gen,og&bvc=vod&nettype=0&bw=323291&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&f=u_0_0&orderid=1,3"],
                            "bandwidth": 323175,
                            "mimeType": "audio/mp4",
                            "mime_type": "audio/mp4",
                            "codecs": "mp4a.40.2",
                            "width": 0,
                            "height": 0,
                            "frameRate": "",
                            "frame_rate": "",
                            "sar": "",
                            "startWithSap": 0,
                            "start_with_sap": 0,
                            "SegmentBase": {
                                "Initialization": "0-781",
                                "indexRange": "782-8837"
                            },
                            "segment_base": {
                                "initialization": "0-781",
                                "index_range": "782-8837"
                            },
                            "codecid": 0
                        }, {
                            "id": 30280,
                            "baseUrl": "https://xy183x232x204x4xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30280.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=323291&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=1378ea&traceid=trlnAWzYpXjrvA_0_e_N&uipk=5&uparams=e%2Ctrid%2Cmid%2Cnbs%2Cuipk%2Cgen%2Cog%2Coi%2Cdeadline%2Cplatform%2Cos&upsig=790b6542d0d0938af0d225dc044ca26a",
                            "base_url": "https://xy183x232x204x4xy.mcdn.bilivideo.cn:8082/v1/resource/30590959941-1-30280.m4s?agrr=0&build=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&bvc=vod&bw=323291&cdnid=10210&deadline=1751432217&dl=0&e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M%3D&f=u_0_0&gen=playurlv3&mid=1393126795&nbs=1&nettype=0&og=hw&oi=2028943452&orderid=0%2C3&os=bcache&platform=pc&sign=1378ea&traceid=trlnAWzYpXjrvA_0_e_N&uipk=5&uparams=e%2Ctrid%2Cmid%2Cnbs%2Cuipk%2Cgen%2Cog%2Coi%2Cdeadline%2Cplatform%2Cos&upsig=790b6542d0d0938af0d225dc044ca26a",
                            "backupUrl": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&nbs=1&uipk=5&gen=playurlv3&og=hw&oi=2028943452&deadline=1751432217&platform=pc&os=bcache&upsig=790b6542d0d0938af0d225dc044ca26a&uparams=e,trid,mid,nbs,uipk,gen,og,oi,deadline,platform,os&cdnid=10210&bvc=vod&nettype=0&bw=323291&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=2028943452&mid=1393126795&deadline=1751432217&uipk=5&gen=playurlv3&og=hw&nbs=1&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&os=08cbv&upsig=56d66068fceb880f6732dcaef8a827e1&uparams=e,oi,mid,deadline,uipk,gen,og,nbs,platform,trid,os&bvc=vod&nettype=0&bw=323291&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=1,3"],
                            "backup_url": ["https://cn-hbwh-cm-01-14.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=0000e9fc696ac5494436a3d8187ebbf80a6u&mid=1393126795&nbs=1&uipk=5&gen=playurlv3&og=hw&oi=2028943452&deadline=1751432217&platform=pc&os=bcache&upsig=790b6542d0d0938af0d225dc044ca26a&uparams=e,trid,mid,nbs,uipk,gen,og,oi,deadline,platform,os&cdnid=10210&bvc=vod&nettype=0&bw=323291&dl=0&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&orderid=0,3", "https://upos-sz-mirror08c.bilivideo.com/upgcxcode/41/99/30590959941/30590959941-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=2028943452&mid=1393126795&deadline=1751432217&uipk=5&gen=playurlv3&og=hw&nbs=1&platform=pc&trid=e9fc696ac5494436a3d8187ebbf80a6u&os=08cbv&upsig=56d66068fceb880f6732dcaef8a827e1&uparams=e,oi,mid,deadline,uipk,gen,og,nbs,platform,trid,os&bvc=vod&nettype=0&bw=323291&f=u_0_0&agrr=0&buvid=F63CEF8A-54B5-3D85-5D3B-235270F9D49C93627infoc&build=0&dl=0&orderid=1,3"],
                            "bandwidth": 323175,
                            "mimeType": "audio/mp4",
                            "mime_type": "audio/mp4",
                            "codecs": "mp4a.40.2",
                            "width": 0,
                            "height": 0,
                            "frameRate": "",
                            "frame_rate": "",
                            "sar": "",
                            "startWithSap": 0,
                            "start_with_sap": 0,
                            "SegmentBase": {
                                "Initialization": "0-781",
                                "indexRange": "782-8837"
                            },
                            "segment_base": {
                                "initialization": "0-781",
                                "index_range": "782-8837"
                            },
                            "codecid": 0
                         
                        }]
}

def download_with_retries(url, temp_filename, desc_text, headers, max_retries=5, timeout=30):
    """Downloads a file with retries, a progress bar, and basic error handling."""
    for attempt in range(max_retries):
        try:
            print(f"Downloading {desc_text.lower()} (Attempt {attempt + 1}/{max_retries})...")
            response = requests.get(url, stream=True, headers=headers, timeout=timeout)
            response.raise_for_status()
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 8192  # 8KB, increased for better performance

            with open(temp_filename, 'wb') as f, tqdm(
                desc=desc_text,
                total=total_size_in_bytes,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(block_size):
                    bar.update(len(data))
                    f.write(data)

            # Verify if the download was complete
            if total_size_in_bytes != 0 and os.path.getsize(temp_filename) != total_size_in_bytes:
                raise IOError("Downloaded file size does not match Content-Length.")
            
            print(f"\nDownload of {desc_text.lower()} successful.")
            return True  # Success
        
        except (requests.exceptions.RequestException, IOError) as e:
            print(f"\nAn error occurred during download: {e}")
            if os.path.exists(temp_filename):
                os.remove(temp_filename)  # Clean up partial file
            if attempt < max_retries - 1:
                print("Retrying...")
            else:
                print(f"Failed to download {desc_text.lower()} after {max_retries} attempts.")
                return False  # Failed after all retries
    return False

def download_and_merge(video_url, audio_url, output_filename):
    """Downloads video and audio with retries, then merges them into a single file."""
    
    # Generate unique temporary filenames
    temp_video_filename = f"{output_filename}.video.tmp"
    temp_audio_filename = f"{output_filename}.audio.tmp"

    try:
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }

        # --- Download Video ---
        video_desc = f"Video: {os.path.basename(output_filename)}"
        if not download_with_retries(video_url, temp_video_filename, video_desc, headers):
            print(f"Failed to download video for {output_filename}. Aborting.")
            return

        # --- Download Audio ---
        audio_desc = f"Audio: {os.path.basename(output_filename)}"
        if not download_with_retries(audio_url, temp_audio_filename, audio_desc, headers):
            print(f"Failed to download audio for {output_filename}. Aborting.")
            return # The video file will be cleaned up in the finally block

        print("Download complete. Merging files...")

        # --- Merge Video and Audio with FFmpeg ---
        merge_command = [
            'ffmpeg',
            '-y',  # Overwrite output file if it exists
            '-i', temp_video_filename,
            '-i', temp_audio_filename,
            '-c', 'copy',  # Copy streams without re-encoding
            output_filename
        ]
        
        # Add a timeout and improved error handling for the merge process
        try:
            subprocess.run(merge_command, check=True, capture_output=True, text=True, timeout=600)
            print(f"Successfully merged. Output file: {output_filename}")
        except subprocess.TimeoutExpired as e:
            print(f"Error: FFmpeg process timed out for {output_filename}.")
            if e.stderr:
                print(f"FFmpeg stderr:\n{e.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error during ffmpeg merging for {output_filename}:")
            print(f"FFmpeg stderr:\n{e.stderr}")

    except Exception as e:
        print(f"An unexpected error occurred during the process for {output_filename}: {e}")
    finally:
        # --- Clean up temporary files ---
        if os.path.exists(temp_video_filename):
            os.remove(temp_video_filename)
        if os.path.exists(temp_audio_filename):
            os.remove(temp_audio_filename)
        print(f"Cleaned up temporary files for {os.path.basename(output_filename)}.")

def batch_download_from_file(file_path, max_workers=5):
    """Reads a file with download tasks and executes them concurrently."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
        return
    
    if not isinstance(tasks, list):
        print(f"Error: The JSON in '{file_path}' should be a list of tasks.")
        return

    tasks_to_run = []
    for task in tasks:
        video_url = task.get('video_url')
        audio_url = task.get('audio_url')
        output_filename = task.get('output_filename')

        if not all([video_url, audio_url, output_filename]):
            print(f"Skipping task due to missing 'video_url', 'audio_url', or 'output_filename': {task}")
            continue
        
        if os.path.exists(output_filename):
            print(f"File '{output_filename}' already exists, skipping download.")
            continue
        tasks_to_run.append(task)

    if not tasks_to_run:
        print("No new tasks to run. All files may already exist.")
        return

    print(f"Found {len(tasks_to_run)} new download tasks. Starting concurrent downloads with {max_workers} workers.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(download_and_merge, task['video_url'], task['audio_url'], task['output_filename']): task
            for task in tasks_to_run
        }

        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            try:
                future.result()
                print(f"Task for '{task.get('output_filename')}' completed successfully.")
            except Exception as exc:
                print(f"Task for '{task.get('output_filename')}' generated an exception: {exc}")
    
    print("\n--- All batch download tasks complete. ---")

if __name__ == "__main__":
    # You can adjust the number of concurrent downloads by changing max_workers
    batch_download_from_file('VAO.txt', max_workers=5)