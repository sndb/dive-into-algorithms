import threading
from time import sleep


def sleep_sort(i):
    sleep(i)
    global sorted_list
    sorted_list.append(i)
    return i


items = [2, 4, 5, 2, 1, 7]
sorted_list = []
[threading.Thread(target=sleep_sort, args=(i,)).start() for i in items]
