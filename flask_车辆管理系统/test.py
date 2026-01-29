# target =6
# nums = [3,2,4]
# def index(nums,target):
#     num1 = set(nums)
#     num2 = set(map(lambda x:target-x,nums))
#     num3 =list(num1&num2)
#     print(num3)
#     if len(num3)<2:
#         return nums.index(num3[0])
#     else:
#         return  nums.index(num3[0]),nums.index(num3[1])
#
# print(index(nums,target))
count = []
# def run(n):
#     # 不走
#     if n <= 0:
#         if n ==0:
#             count.append(n)
#         return
#     # 走一步
#
#     run(n - 1)
#     # 走两步
#     run(n - 2)
#
# # print(run(4))
# run(4)
# print(len(count))

# 1 1 1
# 1 2
# 2 1
#
# 1 1 1 1
# 1 2 1
# 1 1 2
# 2 1 1
# 2 2

# f(n) = f(n−1)+f(n−2)
# 1 1 2 3 5
#






























































#
# print(f(5))


def climbStairs(self, n: int) -> int:
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climbStairs(n - 1) + climbStairs(n - 2)
