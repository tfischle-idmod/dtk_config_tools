from multiprocessing import Pool, TimeoutError
import time
import os


def fct(param):
    print (param)





if __name__ == '__main__':
    # 100 string that should be printed
    strings = ["string" + str(i) for i in range(1,100)]

    # start 4 worker processes
    with Pool(processes=4) as pool:
        pool.map(fct, strings)
