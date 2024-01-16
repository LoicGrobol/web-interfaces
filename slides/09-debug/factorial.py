def factorial(n):
    if n == 0:
        return 1
    res = 1
    for i in range(1, n):
        res = i * res
    return res
    
factorial(9)