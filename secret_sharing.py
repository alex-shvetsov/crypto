from primes import Prime

class Dealer: 
    def __init__(self, k, p, m):
        self.__p = p
        self.__k = k
        self.__m = m
    
    def __gen_point(self):
        point = [self.__m]
        for i in range(self.__k - 1):
            point = point + [Prime.zpelem(self.__p)]
        return point

    def share(self, players):
        # Генерируем точку
        point = self.__gen_point()
        for player in players:
            # Для каждого учатника выичсляем коэффициенты и свободный член
            player.b = 0
            player.factors = []
            for i in range(self.__k):
                a = Prime.zpelem(self.__p)  # a <= Zp
                player.factors.append(a)
                player.b = (player.b + a * point[i]) % self.__p
                
    def __cut(self, matrix):
        # r играет роль номера уравнения и сдвига
        for r in range(self.__k):
            # Умножаем row-е на обратный элемент row-го элемента
            inv = Prime.invert(matrix[r][r], self.__p)
            for c in range(r, len(matrix[r])):
                matrix[r][c] = (matrix[r][c] * inv) % self.__p
            # Обнуляем row-й столбец                
            for nextr in range(r + 1, len(matrix)):
                e = matrix[nextr][r]
                for c in range(r, len(matrix[r])):
                    matrix[nextr][c] = (e * matrix[r][c] * (-1) + matrix[nextr][c]) % self.__p
        return matrix
        
    def recover(self, players):
        if len(players) < self.__k:
            print("Too few players")
            return
                      
        # Формируем систему
        equations = [] 
        for i in range(self.__k):
            equations.append(players[i].factors + [players[i].b])  
        # Лестничный вид
        equations = self.__cut(equations)
        
        # Переворачиваем: x1 <-> xk
        for r in range(len(equations)):
            middle = (len(equations[r]) - 1) // 2
            for c in range(middle):
                t = equations[r][c]
                equations[r][c] = equations[r][len(equations[r])-c-2]
                equations[r][len(equations[r])-c-2] = t
        # Переворачиваем: уравнение_1 <-> уравнение_k
        for r in range(len(equations) // 2):
            t = equations[r]
            equations[r] = equations[len(equations)-r-1]
            equations[len(equations)-r-1] = t
        # Лестничный вид
        equations = self.__cut(equations)
        
        # Последний свободный член
        return equations[self.__k - 1][self.__k]
        
class Player:
    counter = 0
    
    def __init__(self):
        self.secret = 0
        Player.counter += 1
        self.id = Player.counter
        
    def __str__(self):
        return "Player " + str(self.id) 
    
###################################################################################################
m = 41  # secret
k = 3
p = 67
dealer = Dealer(k, p, m)

p1 = Player()
p2 = Player()
p3 = Player()
p4 = Player()
p5 = Player()

plShare = [p1, p2, p3, p4, p5]
plRecover = [p2, p3, p5]

dealer.share(plShare)
print("Secret: " + str(m))

for player in plShare:
    print(str(player) + ": " + str(player.factors) + ", b = " + str(player.b))
    
rm = dealer.recover(plRecover)
print("Secret: " + str(rm))