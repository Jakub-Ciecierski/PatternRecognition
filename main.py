from sys import argv

def fib(n):
    a, b = 0, 1
    while a < n:
        print (a)
        a, b = b, a+b

def args_test(*argv, **keywords):
    for arg in argv:
        print arg
    print '-' * 30
    for key in keywords.keys():
        print key, ":", keywords[key]

'''
fib(10)
'''

def test(a = 1, b = 2, c = 3, d = 4):
    print a,
    print b,
    print c,
    print d,
'''
a = 5;
b = a;
print id(a)
print id(b)

arr1 = [1 , 2, 3]
arr2 = arr1
arr2[0] = 9
print arr1[0]


args_test(1, 2, 5,X="x", Y="y")

d = {25:"25 %s", 35:"35 %s"}
print d[35]
'''

'''
lambda a : a + 5
f = lambda a,b : a+b
print f(5 , 2)
'''

matrix = [[1,2],[3,4]]
print matrix[0][1]

