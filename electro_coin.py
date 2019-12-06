from primes import Prime
from hashlib import sha256
from math import gcd

# little endian

size = 20
 
class Bank:
    __p = Prime.generate(size)  # p
    __q = Prime.generate(size)  # q
    __p_ = Prime.generate(size) # p*
    __q_ = Prime.generate(size) # q*
    __fi = (__p-1)*(__q-1)      # ф(n)
    __fi_ = (__p_-1)*(__q_-1)   # ф(n*)
    n = __p * __q               # n
    n_ = __p_ * __q_            # n*
    pvec = []
    registry = []
    h = 0

    @staticmethod
    def init():
        while(len(Bank.pvec) < 10):
            m = Prime.mutprime(Bank.__fi)
            if m not in Bank.pvec and gcd(m, Bank.__fi_) == 1:
                Bank.pvec.append(m)
        hS = [1 for i in range(len(Bank.pvec))]
        Bank.h = S_to_index(hS)

    @staticmethod
    def f(w):
        m = sha256()
        m.update(int_to_bytes(w))
        return int_from_bytes(m.digest()) % Bank.n
    
    @staticmethod
    def bn_withdraw(client, b):
        summa = S_to_summa(index_to_S(Bank.h))
        assert (client.account >= summa)
        client.account -= summa
        # y = b^(1/h) mod n
        return pow(b, Prime.invert(Bank.h, Bank.__fi), Bank.n)

    @staticmethod
    def bn_change(z, s):
        g = S_to_index(s)
        d = Bank.h // g
        # c = z^(1/d) mpd n*
        return pow(z, Prime.invert(d, Bank.__fi_), Bank.n_)

    @staticmethod
    def bn_put(client, z, N_, a):
        d = 1
        summa = 0
        for i in range(len(a)):
            d *= pow(Bank.pvec[i], a[i])
            summa += (2**i * a[i])
        assert(pow(z, d, Bank.n_) == Bank.f(N_))
        assert(N_ not in Bank.registry)
        Bank.registry.append(N_)
        client.account += summa

    @staticmethod
    def bn_check(l, s, N):
        g = S_to_index(s)
        assert(pow(l, g, Bank.n) == Bank.f(N))
        assert(N not in Bank.registry)
        Bank.registry.append(N)

    @staticmethod
    def process(seller, l, s, N):
        Bank.bn_check(l, s, N)
        summ_s = S_to_summa(s)
        print('На счет продавца зачислена сумма ' + str(summ_s))
        seller.account += summ_s
        print('Счет продавца: ' + str(seller.account))

class Client:
    def __init__(self, account):
        self.account = account
        self.__asbuyer_create_accum() # Создать копилку

    def asbuyer_withdraw(self):
        # Снятие со счета
        N = Prime.zpelem(Bank.n)
        r = Prime.mutprime(Bank.n)
        # b = f(N)*r^h mod n
        b = (Bank.f(N) * pow(r, Bank.h, Bank.n)) % Bank.n
        # A->T: b
        y = Bank.bn_withdraw(self, b)
        # x = y*r^(-1) mod n
        print('Покупатель снял банкноту номиналом ' + str(S_to_summa(index_to_S(Bank.h))))
        return (y * Prime.invert(r, Bank.n)) % Bank.n, N
        # Имеем банкноту (x, N)

    def asbuyer_pay(self, seller, x, N, summa):    
        # Платеж
        s_pay = summa_to_S(summa)               # Номинал оплаты
        g = S_to_index(s_pay)                   # Показатель н. оплаты
        d = Bank.h // g                         # Показатель н. сдачи
        self.__proc_a(d)
        l = pow(x, d, Bank.n)
        r = Prime.mutprime(Bank.n_)
        self.z = self.z * pow(r, d, Bank.n_) % Bank.n_
        # A->B: l,z,s,N
        print('\nПокупатель передает продавцу сумму ' + str(summa))
        print('Счет покупателя: ' + str(self.account))
        c = seller.asseller_receive(l, self.z, s_pay, N)
        zsm = 0
        for i in range(len(self.a)):
            zsm += (2**i * self.a[i])
        print('Сдача в копилке: ' + str(zsm))
        self.z = (c * Prime.invert(r, Bank.n_)) % Bank.n_ 

    def __asbuyer_create_accum(self):
        self.N_ = Prime.zpelem(Bank.n_)     # Номер банкноты-копилки
        self.z = Bank.f(self.N_)
        self.a = [0 for i in range(len(Bank.pvec))]

    def __proc_a(self, d):
        for i in range(len(Bank.pvec)):
            if d % Bank.pvec[i] == 0:
                self.a[i] += 1

    def asbuyer_put(self):
        # A->T: z, N*, a1, a2, ...
        Bank.bn_put(self, self.z, self.N_, self.a)
        print('\nСдача из копилки зачислена на счет покупателя')

    def asseller_receive(self, l, z, s, N):
        # B->T: l,z,s,N
        Bank.process(self, l, s, N)
        return Bank.bn_change(z, s)

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def summa_to_S(summa):
    assert(summa > 0)
    S = []
    while summa > 0:
        S.append(summa % 2)
        summa //= 2
    return S

def S_to_index(S):
    index = 1
    for i in range(len(S)):
        index *= pow(Bank.pvec[i], S[i])
    return index

def index_to_S(index):
    assert(index > 0)
    S = []
    for p in Bank.pvec:
        if index % p == 0:
            index //=p
            S.append(1)
        else:
            S.append(0)
    return S

def S_to_summa(S):
    summa = 0
    for i in range(len(S)):
        summa <<= 1
        summa += S[len(S)-i-1]
    return summa

Bank.init()
buyer = Client(10000)
seller = Client(0)

print('Счет покупателя до: ' + str(buyer.account))
print('Счет продавца до: ' + str(seller.account))
x1, N1 = buyer.asbuyer_withdraw()
x2, N2 = buyer.asbuyer_withdraw()
buyer.asbuyer_pay(seller, x1, N1, 50)
buyer.asbuyer_pay(seller, x2, N2, 900)
buyer.asbuyer_put()
print('\nСчет покупателя после: ' + str(buyer.account))
print('Счет продавца после: ' + str(seller.account))






