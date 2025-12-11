import os  # 导入操作系统相关的模块，用于处理文件路径
import requests  # 导入requests库，用于发送HTTP请求（注意：代码中缺少这个导入）
import json  # 导入json模块，用于解析JSON数据（注意：代码中缺少这个导入）
# 定义下载文件的函数
def downloadFile( url ):
	filename = os.path.basename(url)  # 从URL中提取文件名
	r = requests.get(url)  # 发送GET请求获取文件内容
	with open("./book/" + filename, "wb") as code:  # 以二进制写入模式打开文件
		code.write(r.content)  # 将请求获得的内容写入文件

# 打开并读取书籍列表文件
with open("./bookLists.txt",'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)  # 将JSON文件内容解析为Python字典

bookLists = load_dict['data']['normalBooksInfo']  # 从字典中获取书籍信息列表
bookLen = len(bookLists);  # 获取书籍总数
nowIndex = 0;  # 初始化当前下载索引

# 遍历每本书的信息
for i in bookLists:
	nowIndex = nowIndex +1;  # 当前下载序号递增
	print( "正在下载", ("{}/{}").format(nowIndex,bookLen) );  # 显示下载进度
	print(" id ：", i['id']);  # 打印书籍ID
	print("标题：", i['title']);  # 打印书籍标题
	print("词数：", i['wordNum']);  # 打印书籍词数
	fileUrl = i['offlinedata'];  # 获取书籍下载链接
	print("地址：", fileUrl);  # 打印下载地址
	downloadFile( fileUrl );  # 调用下载函数下载文件
	print("==  下载完成  ==")  # 打印下载完成提示
	print();  # 打印空行，用于格式化输出