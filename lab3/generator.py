import random
import sys

size = int(sys.argv[1])
print(size)

for _ in range(0, size):
    print(str(random.randint(0 , 92233)) + "; " +
        str(random.randint(0 , 92233)) + "; " +
        str(random.randint(0 , 92233)) + "; " +
        str(random.randint(0 , 9223372036854775800)))
