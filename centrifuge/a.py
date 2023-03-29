h=2*3*5*7

for i in range(h):
    char = '.'
    if i%(h/7)==(0*h/3)%(h/7):
        char = '7'
    if i%(h/5)==(1*h/3)%(h/5):
        char = '5'
    if i%(h/2)==(2*h/3)%(h/2):
        char = '2'
    print(char if i%(h/3)!=0 else '.', end='')
