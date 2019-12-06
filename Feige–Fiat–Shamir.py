from primes import Prime
from random import randint

class TrustCentre:
    def __init__(self, size):
        self.__p = self.__gen_blume(size)
        self.__q = self.__gen_blume(size)
        self.n = self.__p * self.__q
        self.__dict = {}
        print('p = ' + str(self.__p))
        print('q = ' + str(self.__q))
        print('n = ' + str(self.n))
        
    def __gen_blume(self, size):
        p = 0
        while (p - 3) % 4 != 0:
            p = Prime.generate(size)
        return p
    
    def register(self, sub):
        self.__dict[sub.id] = sub
        print('Зарегистрировано!')
            
    def get_subs(self):
        return self.__dict
    
    def __str__(self):
        s = '\nАбоненты:\n'
        s += '-' * 30
        for key, value in self.__dict.items():
            s += '\nid: ' + str(key)
            s += '\nkey:\n' + str(value.I) + '\n'
            s += '-' * 30
        return s
    
class Sub:   
    __sid = 0
    
    def __init__(self, n, k):
        Sub.__sid += 1
        self.id = Sub.__sid
        self.init(n, k)
        
    def init(self, n, k):
        self.__n = n
        self.__k = k
        self.__S = [Prime.mutprime(n) for i in range(k)]
        signs = [pow(-1, randint(0, 1)) for i in range(k)]
        self.I = [signs[i] * Prime.invert(pow(self.__S[i], 2), n) for i in range(k)]
        
    def get_xy(self, e):
        # Генерация x
        r = Prime.zpelem(self.__n)
        x = pow(-1, randint(0, 1)) * pow(r, 2) % self.__n
        
        # Вычисление y
        S = 1
        for i in range(self.__k):
            if e[i] == 1:
                S = S * self.__S[i]
        y = (r * S) % self.__n
    
        print('\nДоказывающий генерирует x, вычисляет y и отправляет x и y проверяющему.')
        print('r = ' + str(r))
        print('x = ' + str(x))
        print('s = ' + str(self.__S))
        print('y = ' + str(y))
        return x, y
    
    def gen_bool(self):
        self.__e = [randint(0, 1) for i in range(self.__k)]
        print('Проверяющий генерирует булев вектор и отправляет доказывающему.')
        print('e = ' + str(self.__e))
        return self.__e
    
    def get_x_(self, y, prover_id, tc):
        I = 1
        key = tc.get_subs()[prover_id].I
        key[0] += 1 
        for i in range(self.__k):
            if self.__e[i] == 1:
                I = I * key[i]
        x_ = (pow(y, 2) * I) % self.__n
        print('\nПроверяющий получает открытый ключ доказывающего из центра доверия,')
        print('вычисляет x_ и сравнивает его с x, полученным от доказывающего.')
        print('I = ' + str(key))
        return x_
    
size = input('Центр доверия. Размер чисел Блюма [бит]: ')
tc = TrustCentre(int(size))

k = int(input('k = '))

flag = True
while flag:
    s = input('Действие:\n0 - Новый абонент\n1 - Продолжить\nВыбор: ')
    if s == '0':
        tc.register(Sub(tc.n, k))
        print(tc)
    elif s == '1' and len(tc.get_subs()) >= 2:
        flag = False
        
print('\nВыберите доказывающего и проверяющего абонентов.')
print(tc)

prover_id = verifier_id = 0
prover = None
verifier = None

flag = True
while flag:
    prover_id = int(input('ID доказывющего: '))
    if prover_id in tc.get_subs():
        prover = tc.get_subs()[prover_id]
        flag = False
        
flag = True
while flag:
    verifier_id = int(input('ID проверяющего: '))
    if verifier_id in tc.get_subs() and verifier_id != prover_id:
        verifier = tc.get_subs()[verifier_id]
        flag = False
    
t = int(input('t = '))

succ = True
for i in range(t):
    print('\nПопытка ' + str(i + 1))
    print('-' * 30)
    print('n = ' + str(tc.n))
    unit = randint(0, 1)
    e = verifier.gen_bool()
    x, y = prover.get_xy(e)
    x_ = verifier.get_x_(y, prover_id, tc)
    succ = (x == x_ % tc.n or x == -x_ % tc.n)
    print('x = ' + str(x))
    print('x_ = ' + str(x_))
    print('Результат: ' + str(succ))
    if not succ:
        break

if succ:
    print('\nУСПЕХ')
else:
    print('\nНЕУДАЧА')
