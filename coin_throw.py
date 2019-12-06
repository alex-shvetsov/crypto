import hashlib
import random

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

R1 = random.randint(2**40, 2**80)
R2 = random.randint(2**40, 2**60)
print('R1 = ' + hex(R1))
print('R2 = ' + hex(R2))

print('Алиса бросает монету и вычисляет хэш!')
b = 0
p = random.random()
if p >= 0.5:
    b = 1
print('b = ' + str(b))

# Конкатенация R2 || b
R2_bc = (R2 << 1) + b
R2_bc_bytes = int_to_bytes(R2_bc)

# Конкатенация R1 || R2 || b
R1_bytes = int_to_bytes(R1)
R1R2b = R1_bytes + R2_bc_bytes

# Алиса вычисляет хэш
h1 = hashlib.sha256()
h1.update(R1R2b)
r = h1.hexdigest()
print('Хэш: ' + r)        

print('\nАлиса отправила R1 и r Бобу!')

# Боб делает догадку
print('\nБоб сделал догадку и отправил c Алисе!')
c = 0
p = random.random()
if p >= 0.5:
    c = 1
print('c = ' + str(c))

# Алиса узнает результат жеребьевки
print('\nАлиса проверяет, угадал ли Боб!')
print('b = c: ' + str(b == c))

# Возможно, Алиса захочет соврать
lie = random.random()
if lie < 0.5:
    print('\n###########################')
    print('Алиса решила соврать!')
    b = 0 if b == 1 else 1
    print('Она изменила b = ' + str(b))
    R2_bc = (R2 << 1) + b
    R2_bc_bytes = int_to_bytes(R2_bc)
    R1R2b = R1_bytes + R2_bc_bytes
    print('###########################')

print('\nАлиса отправляет R2 и b Бобу!')

# Боб вычисляет хэш
h2 = hashlib.sha256()
h2.update(R1R2b)
t = h2.hexdigest()

print('\nБоб вычисляет хэш!')
print('Хэш: ' + t)
if t != r:
    print('Хэши не совпадают. Алиса наврала!')
else:
    print('Хэши совпадают. Алиса не наврала!')
    print('Боб проверяет, угадал ли он!')
    print('b = c: ' + str(b == c))