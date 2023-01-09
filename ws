from typing import List
from random import randint


class MyException(Exception):
    pass

class BoardOutException(MyException):
    def __init__(self, expression:str, message:str) -> None:
        self.expression = 'BoardOutException: ' + expression
        self.message = message

class ShipAddCollizion(MyException):
    def __init__(self, expression:str, message:str) -> None:
        self.expression = 'ShipAddCollizion: ' + expression
        self.message = message

class ShootCollizion(MyException):
    def __init__(self, expression:str, message:str) -> None:
        self.expression = 'ShootCollizion: ' + expression
        self.message = message


class Dot():
    def __init__(self, x:int, y:int, symbol:str='O') -> None:
        self.x = x
        self.y = y
        self.symbol = symbol

    # def __init__(self, dot:object) -> None:
    #     self.x = dot.x
    #     self.y = dot.y
    #     self.symbol = dot.symbol

    def __eq__(self, o) -> bool:
        return self.x == o.x and self.y == o.y

    def __str__(self) -> str:
        return self.symbol


class Ship():
    def __init__(self, lenght:int, start:Dot, dir:str) -> None:
        self.lenght = lenght
        self.alive = lenght
        self.dots = []

        for i in range(lenght):
            if dir == "horizontal":
                self.dots.append(Dot(start.x+i,start.y,"■"))
            if dir == "vertical":
                self.dots.append(Dot(start.x,start.y+i,"■"))


class Field ():
    
    field = "0|1|2|3|4|5|6|\n" \
            "1|{0}|{1}|{2}|{3}|{4}|{5}|\n" \
            "2|{6}|{7}|{8}|{9}|{10}|{11}|\n" \
            "3|{12}|{13}|{14}|{15}|{16}|{17}|\n" \
            "4|{18}|{19}|{20}|{21}|{22}|{23}|\n" \
            "5|{24}|{25}|{26}|{27}|{28}|{29}|\n" \
            "6|{30}|{31}|{32}|{33}|{34}|{35}|"

    def print(self, matrix:List[List[str]], hid:bool) -> None:
        if hid == False:
            print(self.field.format(*[matrix[i][j] for j in range(6) for i in range(6)]))
        else: 
            print(self.field.format(*[('O' if (matrix[i][j].symbol == '■') else matrix[i][j]) for j in range(6) for i in range(6)]))



class Board():
    def __init__(self, hid:bool) -> None:
        self.matrix = [[Dot(i, j) for j in range(6)] for i in range(6)]
        self.ships = []
        self.hid = hid
        self.aliveShips = 0
        self.field = Field()

    def add_ship(self, lenght:int, start:Dot, dir:str) -> bool:
        try:
            if start.x > 5 or start.y > 5 or start.x < 0 or start.y < 0 :
               raise BoardOutException('start:Dot error','вы поставили точку за границу')

            if (start.x+lenght-1 if dir == "horizontal" else start.y+lenght-1) > 5:
               raise BoardOutException('start:Dot and lenght:int error','вы поставили точку за границу')

            # =====            
            if dir == "horizontal":
                for i in range(lenght):
                    for dx, dy in [(0, 0), (1, 0), (0, 1), (1, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1)]:
                        x = start.x + i + dx
                        y = start.y + dy

                        if x >= 0 and x <= 5 and y >= 0 and y <= 5 and self.matrix[x][y].symbol == '■':
                            raise ShipAddCollizion('ship collision error', f'столкновение')
            else:
                for i in range(lenght):
                    for dx, dy in [(0, 0), (1, 0), (0, 1), (1, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1)]:
                        x = start.x + dx
                        y = start.y + i + dy

                        if x >= 0 and x <= 5 and y >= 0 and y <= 5 and self.matrix[x][y].symbol == '■':
                            raise ShipAddCollizion('ship collision error', f'столкновение')
            # =====

        except BoardOutException as e:
            print(e.expression, e.message)
            return False

        except ShipAddCollizion as e:
            print(e.expression, e.message)
            return False

        else:
            ship = Ship(lenght, start, dir)
            self.ships.append(ship)
            self.aliveShips += 1

            for dot in ship.dots:
                x, y = dot.x, dot.y
                self.matrix[x][y] = dot

            return True

    def shoot(self, dot:Dot) -> bool:
        try:
            if dot.x > 5 or dot.y > 5 or dot.x < 0 or dot.y < 0 :
                raise BoardOutException('dot:Dot error','Выберите точку на поле')

            if self.matrix[dot.x][dot.y].symbol == 'T' or self.matrix[dot.x][dot.y].symbol == 'X': 
                raise ShootCollizion('dot:Dot error','Выберите другую точку на поле')

        except BoardOutException as e:
            print(e.expression, e.message)

        except ShootCollizion as e:
            print(e.expression, e.message)

        else:
            if self.matrix[dot.x][dot.y].symbol == '■':
                self.matrix[dot.x][dot.y].symbol = 'X'

                for i in self.ships:
                    if dot in i.dots:
                        i.alive -= 1

                        if i.alive == 0:
                            self.aliveShips -= 1

                        break   

                return True
            else:
                self.matrix[dot.x][dot.y].symbol = 'T'
                return False

    def print(self):
        self.field.print(self.matrix, self.hid)



class Player():
    def __init__(self) -> None:
        self.myboard = Board(False)
        self.enemyboard = Board(True)

    def ask(self) -> Dot:
        pass

    def move(self) -> bool:
        dot = self.ask()

        try:
            return self.enemyboard.shoot(dot)
            
        except:
            self.move()

class User(Player):
    def __init__(self) -> None:
        super().__init__()

    def ask(self) -> Dot:
        text = list(map(int, input("Ваш выстрел (две координаты через пробел): ").split()))
        return Dot(text[0] - 1, text[1] - 1)

class AI(Player):
    def __init__(self) -> None:
        super().__init__()
        
    def ask(self) -> Dot:
        avaliableShots = [self.enemyboard.matrix[i][j] for j in range(6) for i in range(6)]
        
        for i in avaliableShots:
            if i.symbol in ('T', 'X'):
                avaliableShots.remove(i)

        return avaliableShots[randint(0, len(avaliableShots)-1)]



class Game():
    def __init__(self) -> None:
        self.user = User()
        self.ai = AI()
    
    def start(self):
        self.user.myboard = self.randomBoard()
        self.ai.myboard = self.randomBoard()        
        
        self.user.enemyboard = self.ai.myboard
        self.ai.enemyboard = self.user.myboard
        self.user.enemyboard.hid = True

        self.greet()
        self.loop()

    def greet(self):
        print("Привет, пользователь! \nДанные вводятся в формате х у, через пробел")

    def check(self) -> bool:
        if self.user.myboard.aliveShips == 0:
            print("Вы проиграли!")
            return True

        if self.user.enemyboard.aliveShips == 0:
            print("Вы выиграли!")
            return True    

    def globalMove(self, mode:bool) -> bool:
        flag = True # за повтор ходов
        finish = False # за окончание игры

        while flag:
            flag = self.user.move() if mode else self.ai.move() # проверка по ходу
            finish = self.check() # проверка по игре

            if flag and not finish:
                print("Попадание, еще один ход ваш:")
                self.ai.myboard.print()

            if finish:
                break
        
        return finish

    def loop(self):
        cnt = 1
        flag = True

        while True:
            print(f"Ход: {cnt}")
            
            print("Наша доска")
            self.user.myboard.print()
            print('')

            print("Вражеская доска")
            self.user.enemyboard.print()
            print('')
            
            if self.globalMove(flag):
                break

            flag = not flag

            cnt += 1

    def randomBoard(self) -> Board:
        ships = {
            3:1,
            2:2,
            1:4
        }

        retBoard = Board(False)

        for length in ships.keys():
            for cnt in range(ships[length]):
                i = 0

                while not retBoard.add_ship(length, Dot(randint(0,5),randint(0,5)), ["horizontal","vertical"][randint(0,1)]):
                    i += 1

                    if i > 100:
                        print("================================================================")
                        return self.randomBoard()
        
        return retBoard
              

game = Game()

game.start()              
