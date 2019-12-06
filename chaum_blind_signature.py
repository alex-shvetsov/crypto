# Слепая подпись Шаума - RSA

# (n, e) - открытый ключ 
# (n, d) - закрытый ключ 
# n = pq, q != p, p и q - б.п.ч.
# e: (e, ф(n)) = 1
# d: e^(-1) mod ф(n)
# x - сообщение на подпись

import random
import math

# Функция Эйлера
def eul(n):
    amount = 0        
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount

# Генерация простого числа (тест Миллера-Рабина)
def rpr(): 
    def is_prime(n):
        if n!=int(n):
            return False
        n=int(n)
    
        if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
            return False
     
        if n==2 or n==3 or n==5 or n==7:
            return True
        s = 0
        d = n-1
        while d%2==0:
            d>>=1
            s+=1
        assert(2**s * d == n-1)
     
        def trial_composite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, n) == n-1:
                    return False
            return True  
     
        for i in range(8):
            a = random.randrange(2, n)
            if trial_composite(a):
                return False
     
        return True 
    
    a = 0
    while not is_prime(a):
        a = random.randint(2, 499)
    return a

# Поиск числа, взаимно простого с p   
def rmutpr(p):
    if p < 3:
        return 1
    a = 0
    while math.gcd(a, p) != 1:
        a = random.randint(2, p - 1)
    return a

# Обратный по модулю
def inv(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)
    
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Нет обратного')
    else:
        return x % m
    
#______________________________________________________

# Генерация n = pq
p = q = 0
while p == q:
    p = rpr()
    q = rpr()
n = p * q

# Вычисление ϕ(n), генерация e и d
ϕ = eul(n)
e = rmutpr(ϕ)

print('n = ' + hex(n))

# Сообщение
x = 0xabcd
print('Сообщение x = ' + hex(x))

# Шифрование
# y = (x * k^e) mod n
# k ∈ Zn*
k = rmutpr(n)
y = (x * pow(k, e, n)) % n
print('Зашифрованное сообщение y = ' + hex(y))
print('Алиса посылает Бобу y, e и n!')

print('\nБоб вычисляет d с помощью e и n!')
d = inv(e, ϕ) 

print('Боб подписывает сообщение!')
# Подписание
# z = y^d mod n
z = pow(y, d, n)
print('Боб отправляет Алисе подписанное сообщение z = ' + hex(z))

# Расшифрование и получение подписи
# s = (z * k^(-1)) mod n
s = (z * inv(k, n)) % n
print('Алиса расшифровывает подпись s = ' + hex(s))

# Проверка 
# s ≡ z * k^(-1) ≡ y^d * k^(-1) ≡ x^d * k^(ed) * k^(-1) ≡ x^d * k * k^(-1) ≡ x^d (mod n)
print('x^d (mod n) = ' + hex(pow(x, d, n)))
print('s = ' + hex(s))
print(pow(x, d, n) == s)
