# 打印乘法表

# for i in range(1,10):
#     for j in range(1,10):
#         if j <= i:
#             print(str(i) + '*' + str(j) + '=' + str(i * j), end='\t')
#     print()

for i in range(1,10):
    for j in range(1,i+1):
        print(f"i的值为：{i}")
        print(f"j的值为：{j}")
    
    