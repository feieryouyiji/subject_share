def gen():
    yield 1
    yield 2
    yield 3
g = gen()
print(g)
print(next(g), '<g1')
print(next(g), '<g2')
print(next(g), '<g3')
print(next(g), '<g3')