

#q1
print("question 1")
fibonacci = lambda n, a=0, b=1: [a] + fibonacci(n-1, b, a+b) if n > 0 else []
print(fibonacci(10))
print("----------------------------------------------------------")

#q2
print("question 2")
concat_strings = lambda lst: '' if not lst else lst[0] + (' ' + concat_strings(lst[1:]) if len(lst) > 1 else '')
print(concat_strings(["hello", "world", "in", "lambda"]))
print("----------------------------------------------------------")

#q3
print("question 3")
cumulative_sum_of_squares = lambda lsts: list(map(lambda sublist: sum(map(lambda x: x**2, filter(lambda y: y % 2 == 0, sublist))), lsts))
print(cumulative_sum_of_squares([[1, 2, 3], [4, 5, 6], [7, 8]]))
print("----------------------------------------------------------")

#q4
print("question 4")
cumulative_op = lambda op: lambda seq: seq[0] if len(seq) == 1 else op(seq[0], cumulative_op(op)(seq[1:]))
factorial = lambda n: cumulative_op(lambda x, y: x * y)(list(range(1, n + 1)))
exponentiation = lambda base, exp: cumulative_op(lambda x, y: x * y)([base] * exp)
print(factorial(5))  #הפונקציה עושה עצרת
print(exponentiation(2, 3))  #הפונקציה עושה 2 בחזקת 3
print("----------------------------------------------------------")

#q5
print("question 5")
from functools import reduce
result = reduce(lambda x, y: x + y, map(lambda z: z**2, filter(lambda n: n % 2 == 0, [1, 2, 3, 4, 5, 6])))
print(result)
print("----------------------------------------------------------")

#q6
print("question 6")
palindrome_count = lambda lst: list(map(lambda sublst: sum(map(lambda s: s == s[::-1], sublst)), lst))
print(palindrome_count([["madam", "test","abba"], ["level", "world"], ["noon", "not"]]))
print("----------------------------------------------------------")

#q7
print("question 7")
print("""
Eager Evaluation:
When we use eager evaluation, all computations are done immediately when we request the values.\nAll results are stored in memory while the code is running.\nFor example, if there’s a function that generates a series of numbers, eager evaluation will compute all the numbers in the series and store the results in memory right away.

Lazy Evaluation:
When we use lazy evaluation, computations are done only when we need the values.\nThe results are not all stored in memory right away; instead, they are computed on demand.\nThis means values are computed only as needed, which can save memory if there are a lot of values.
""")
print("----------------------------------------------------------")

#q8
print("question 8")
primes_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % d != 0 for d in range(2, int(x**0.5) + 1))], reverse=True)
print(primes_desc([10, 3, 5, 7, 2, 11, 13]))  # Example output: [13, 11, 7, 5, 3, 2]
print("----------------------------------------------------------")
