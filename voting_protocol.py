#Протокол голосования с двумя центральными комиссиями

from primes import Prime

def encrypt(mes, o_key, mod):
    return pow(mes, o_key, mod)

def decrypt(mes, s_key, mod):
    return pow(mes, s_key, mod)

p = Prime.generate(240)
q = Prime.generate(240)
n = p * q
n_ = (p-1)*(q-1)
size = 20

class T1:
    # Центральное управление регистрами
    N = 0   # Сообщение с номерами участников
    
    @staticmethod
    def reg_id(key):
        # Выдача рагистрационного номера
        Ni = Prime.generate(size)
        T1.N = ((T1.N << size) + Ni) % n  
        return encrypt(Ni, key, n)
    
    @staticmethod
    def create_N():
        print('\nT1 отправил T2 рег. номера участников')
        return encrypt(T1.N, T2.K1, n)
    
class T2:
    # Центральная избирательная комиссия
    N = []  # Список всех N, полученный от T1 
    K1 = Prime.mutprime(n_)          # Открытый ключ
    K2 = Prime.invert(K1, n_)        # Секретный ключ
    I = []  # Список проголосовавших
    C = []  # Список зашифрованных голосов участников
    candidates = []  # Список кандидатов
        
    @staticmethod 
    def get_N(M):
        dN = decrypt(M, T2.K2, n)
        while dN > 0:
            Ni = dN % (2**size)
            T2.N.append(Ni)
            dN >>= size
    
    @staticmethod    
    def check_C(nQ):
        for Ci in T2.C:
            Bi = decrypt(Ci, T2.K2, n)
            Ii = Bi >> (size + nQ)
            Bi %= 2**(size + nQ)
            Ni = Bi >> nQ
            assert(Ni in T2.N)
            T2.N.remove(Ni)
            T2.I.append(Ii)
            Bi %= 2**nQ
            for i in range(nQ):
                b = (Bi >> (nQ - i - 1)) % 2
                if (b == 1):
                    T2.candidates[i] += 1
                    break
        
    
class A:
    def __init__(self):
        self.K1 = Prime.mutprime(n_)            # Открытый ключ
        self.K2 = Prime.invert(self.K1, n_)     # Секретный ключ
    
    def get_id(self):
        self.Ni = decrypt(T1.reg_id(self.K1), self.K2, n)
        print('Участник получил регистрационный номер ' + str(self.Ni))
        
    def create_B(self, nQ):
        Ii = Prime.generate(size)
        Bi = (Ii << size) + self.Ni
        for i in range(nQ):
            Bi <<= 1
            if (i == self.v - 1):
                Bi += 1
        print('Участник с ID ' + str(Ii) + ' отправляет T2 сообщение с голосом')
        Ci = encrypt(Bi, T2.K1, n)
        T2.C.append(Ci)
  
print('Количество кандидатов:')
nQ = int(input())
    
lA = []
print('Количество участников:')
nA = int(input())

for i in range(nA): 
    a = A()
    a.get_id()
    lA.append(a)
    print('Участник ' + str(i+1) + ' голосует за [1 - ' + str(nQ) +']:')
    a.v = int(input())
    
# Иниц. списка кандидатов, у всех изначально 0
T2.candidates = [0 for i in range(nQ)]  
    
# T1 шифрует N и отправляет T2
T2.get_N(T1.create_N())

# Каждый A формирует сообщение Bi, шифрует его и отправляет T2
for i in range(nA):
    lA[i].create_B(nQ)
    
print('T2 расшифровывает сообщения от участников, проверяет рег. номера по полученному списку,')
print('добавляет идентификатор к списку проголосовавших')
T2.check_C(nQ);

print('\nУчастники:')
for i in range(len(T2.I)):
    print('Участник ' + str(i+1) + ': ' + str(T2.I[i]))
print('\nРезультаты:')
for i in range(len(T2.candidates)):
    print('Голосов за кандидата ' + str(i+1) + ': ' + str(T2.candidates[i]))
