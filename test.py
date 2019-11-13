from threading import Timer
from itertools import product
from random import shuffle

RANKS = ['2', '3','4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['H', 'D', 'S', 'C'] # Heart-H, Diamond-D, Spade-S, Club-C

DECK = list(product(RANKS, SUITS))

# def ac():
#
#
#
# action = input("Enter: ")
# nTimer = Timer(3,ac())
# nTimer.join()

# from datetime import datetime
# from threading import Timer
# # 打印时间函数
# def printTime(inc):
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     t = Timer(inc, printTime, (inc,))
#     t.start()
# # 5s
# printTime(1)

# import time
# import timeout_decorator
#
# @timeout_decorator.timeout(3, use_signals=False)
# def mytest():
#     action = input("Enter a number: ")
#     return action
#
#
# def get():
#     action = ""
#     try:
#         action = mytest()
#     except timeout_decorator.TimeoutError:
#         action = 'f'
#
#     print(action)
#
#
#
# import time
# import timeout_decorator
#
# @timeout_decorator.timeout(3)
# def mytest():
#     time.sleep(5)
#     return 5
# # mytest()
# if __name__ == '__main__':
#     mytest()

# import time
# from func_timeout import func_set_timeout
# import func_timeout
#
# @func_set_timeout(5)
# def task():
#     action = input("Enter")
#     return action
#
# def get():
#     action = ""
#     try:
#         action = task()
#     except func_timeout.exceptions.FunctionTimedOut:
#         action = 'f'
#     return action
#
# print(get())
# card = input("Enter: ")
# print(type(card))

print(DECK.pop())

shuffle(DECK)

cards = DECK[0:1]
for i in range(0, len(cards)):
    print("     ______ ", end="")
print()
for i in range(0, len(cards)):
    if len(cards[i][0]) == 1:
        print("    |"+cards[i][0]+"     |", end="")
    else:
        print("    |"+cards[i][0]+"    |", end="")

print()
for i in range(0, len(cards)):
    print("    |      |", end="")
print()
for i in range(0, len(cards)):
    print("    |      |", end="")
print()
for i in range(0, len(cards)):
    print("    |     "+cards[i][1]+"|", end="")
print()
for i in range(0, len(cards)):
    print("     ------ ", end="")
print()
for i in range(0, len(cards)):
    print("       "+str(i+1)+"    ", end="")
