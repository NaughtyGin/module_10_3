import threading
from time import sleep
from random import randint


class Bank:

    def __init__(self, balance=0):
        super().__init__()
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self):
        dep_count = 0
        for i in range(100):
            dep_num = randint(50, 500)
            dep_count = dep_count + 1
            print(f'Запрос на пополнение № {dep_count}: {dep_num}, система блокирована: {self.lock.locked()}.')
            try:
                if self.balance >= 500 and self.lock.locked():
                    self.lock.release()
            finally:
                self.balance = self.balance + dep_num
                print(f'Пополнение: {dep_num}. Баланс: {self.balance}.')
                sleep(0.001)

    def take(self):
        take_count = 0
        for i in range(100):
            take_num = randint(50, 500)
            take_count = take_count + 1
            print(f'Запрос № {take_count} на снятие {take_num}.')
            if take_num <= self.balance:
                self.balance = self.balance - take_num
                print(f'Снятие: {take_num}. Баланс: {self.balance}.')
            else:
                self.lock.acquire()
                print('Запрос отклонён, недостаточно средств.')
            sleep(0.001)


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
