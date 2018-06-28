import random
import math

tryAgain = True

def montePi (numDarts):
    inCircle = 0

    for i in range(numDarts):
        x = random.random()
        y = random.random()
        d = math.sqrt(x**2 + y**2)

        if d <= 1:
            inCircle = inCircle + 1
    
    pi = inCircle/numDarts * 4

    return pi

while (tryAgain == True):
    numDarts = int(input('Enter a number of darts! '))
    print('The approximation of pi is: ', montePi(numDarts))
    msg = input('Want to do it again? Y/n')
    if msg == 'y':
        pass
    else:
        break
