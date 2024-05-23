"""
两个相差为2的素数称为素数对，如5和7,17和19等，本题目要求找出所有两个数均不大于n的素数对。
输入：
一个正整数n。1<=n<=10000。
输出：
所有小于等于n的素数对。每对素数对输出一行，中间用单个空格隔开。若没有找到任何素数对，输出empty。
"""
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_prime_pairs(n):
    prime_pairs = []
    for i in range(2, n+1):
        if is_prime(i) and is_prime(i+2):
            prime_pairs.append((i, i+2))
    return prime_pairs

n = int(input("请输入一个正整数n："))

pairs = find_prime_pairs(n)

if pairs:
    for pair in pairs:
        print(pair[0], pair[1])
else:
    print("empty")
    