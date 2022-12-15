A_0 = 722
B_0 = 354

A_MUL = 16807
B_MUL = 48271
MOD = 2147483647

def is_match(a, b):
    return (a%(2**16)) == (b%(2**16))

def part1Answer():
    a, b = A_0, B_0
    count = 0
    for i in range(40000000):
        a, b = (a*A_MUL)%MOD, (b*B_MUL)%MOD
        if is_match(a, b):
            count += 1
    return count

def part2Answer():
    a, b = A_0, B_0
    count = 0
    for i in range(5000000):
        a, b = (a*A_MUL)%MOD, (b*B_MUL)%MOD
        while a%4 != 0:
            a = (a*A_MUL)%MOD
        while b%8 != 0:
            b = (b*B_MUL)%MOD
        if is_match(a, b):
            count += 1
    return count

if __name__ == "__main__":
    print("Part 1: {}".format(part1Answer()))
    print("Part 2: {}".format(part2Answer()))

