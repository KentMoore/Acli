# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # 自动下载对应版本的ChromeDriver并启动
# browser = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install())
# )

# # 测试是否正常工作（可选）
# browser.get("https://www.baidu.com")
# print(browser.title)
# browser.quit()


from DrissionPage import ChromiumPage

# 初始化 (自动连接本地 Chrome，无需 Service 或 Manager)
page = ChromiumPage()

# 打开网页
page.get("https://www.baidu.com")

# 打印标题
print(page.title)

# 退出
page.quit()