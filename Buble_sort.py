from time import perf_counter
import random


nums = list(range(1000000))
random.shuffle(nums)

# Python сортировка
start = perf_counter()
sorted(nums)
end = perf_counter()
print()
print(f"Питоновская {end-start:.9f}")

# Сортировка Хоара
def Hoara(nums):
    if len(nums) <= 1:
        return nums
    else:
        # q = random.choice(nums)  
        q = nums[len(nums) // 2]  
    l_nums = [n for n in nums if n < q]
    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n > q]
    return Hoara(l_nums) + e_nums + Hoara(b_nums)
start = perf_counter()
Hoara(nums)
end = perf_counter()
print(f"Хоара {end-start:.9f}")