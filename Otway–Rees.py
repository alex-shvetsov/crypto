from random import randint
from primes import Prime
import Crypto.Cipher

def rand(size):
    r = randint(1 << (size*8 - 1), (1 << (size*8)) - 1)
    return r.to_bytes(size, byteorder='big')

def ghex(barr):
    return hex(int.from_bytes(barr, "big"))

def p():
    AID = rand(4)   # Идентификатор Алисы
    BID = rand(4)   # Идентификатор Боба
    SID = rand(8)   # Номер сессии
    
    kA = rand(32)   # Ключ Алисы
    kB = rand(32)   # Ключ Боба
    rA = rand(16)   # Случайное число Алисы
    rB = rand(16)   # Случайное число Боба

    ivA = rand(16)
    ivB = rand(16)
    сtA = AES.new(kA, AES.MODE_CBC, ivA)
    ctB = AES.new(kB, AES.MODE_CBC, ivB)
    
    # Алиса -> {SID, AID, BID, EkA(rA, SID, AID, BID)} -> Боб
    mesA = ctA.encrypt(rA + SID + AID + BID)
    
    # Боб -> {SID, AID, BID, EkA(rA, SID, AID, BID), EkB(rB, SID, AID, BID)} -> Трент
    mesB = ctB.encrypt(rB + SID + AID + BID)
    
    # Трент: расшифрование и сравнение
    dmesA = ctA.decrypt(mesA)
    dmesB = ctB.decrypt(mesB)
    
    ok = SID == dmesA[16:24] == dmesB[16:24] and \
         AID == dmesA[24:28] == dmesB[24:28] and \
         BID == dmesA[28:32] == dmesB[28:32]
         
    if not ok:
        return False
        
    # Трент -> {I, EkA(rA, kS), EkB(rB, kS)} -> Боб
    kS = rand(32)   # Сеансовый ключ
    print('Сеансовый ключ:\n' + ghex(kS))
    mesTA = ctA.encrypt(rA + kS)
    mesTB = ctB.encrypt(rB + kS)
    
    # Боб: расшифрование и сравнение
    dmesTB = ctB.decrypt(mesTB)
    print('Сеансовый ключ, полученный Бобом:\n' + ghex(dmesTB[16:]))
    
    ok = dmesTB[:16] == rB
    
    if not ok:
        return False
    
    # Боб -> {I, EkA(rA, sK)} -> Алиса
    # Алиса: расшифрование и сравнение
    dmesTA = ctA.decrypt(mesTA)
    print('Сеансовый ключ, полученный Алисой:\n' + ghex(dmesTA[16:]))
    
    ok = dmesTA[:16] == rA
    
    if not ok:
        return False
    
    return (dmesTA[16:] == dmesTB[16:] == kS)

if p():
    print('Протокол завершен')
else:
    print('Протокол прерван')
