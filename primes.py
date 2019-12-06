# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:35:19 2019

@author: Lenovo
"""

import math
import random

class Prime:
    
    # Тест на простоту
    @staticmethod
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
    
    # Генерация простого числа заданного размера
    @staticmethod
    def generate(size): 
        a = 0
        while not Prime.is_prime(a):
            a = random.randint(1 << (size-1), (1 << size) - 1)
        return a
    
    # Взаимно простое с p
    @staticmethod
    def mutprime(p):
        if p < 3:
            return 1
        a = 0
        while math.gcd(a, p) != 1:
            a = random.randint(2, p - 1)
        return a
    
    # Случайное из Zp
    @staticmethod
    def zpelem(p):
        return random.randint(1, p - 1)
    
    # Обратный к a по модулю m
    @staticmethod
    def invert(a, m):
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