from multiprocessing import Pool
import time

COUNT = 50000000
def countdown(n):
    while n > 0:
        n -= 1

if __name__ == '__main__':
    pool = Pool(processes=2)
    start = time.time()
    p1 = pool.apply_async(countdown, [COUNT//2])
    p2 = pool.apply_async(countdown, [COUNT//2])
    pool.close()
    pool.join()
    end = time.time()
    print('Elapsed time -', round(end - start, 2))
