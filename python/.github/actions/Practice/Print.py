# 打印乘法表

for i in range(1,10):
    for j in range(1,10):
        if j <= i:
            print(str(i) + '*' + str(j) + '=' + str(i * j), end='\t')
    print()

