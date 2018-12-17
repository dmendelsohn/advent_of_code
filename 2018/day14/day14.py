import argparse

def get_digits(n):
    total = []
    if n == 0:
        return [0]
    while n > 0:
        total.append(n%10)
        n /= 10
    return total[::-1]

def next_recipes(recipes, index0, index1):
    total = recipes[index0] + recipes[index1]
    recipes.extend(get_digits(total))
    index0 = (index0 + recipes[index0] + 1)%len(recipes)
    index1 = (index1 + recipes[index1] + 1)%len(recipes)
    return index0, index1

def part1Answer(n):
    recipes = [3, 7]
    index0, index1 = 0, 1
    while len(recipes) < n+10:
        index0, index1 = next_recipes(recipes, index0, index1)
    return ''.join(map(str, recipes[n:n+10]))

def part2Answer(n):
    recipes = [3,7]
    index0, index1 = 0, 1
    digits_to_match = map(int, list(n))
    while recipes[-len(digits_to_match):] != digits_to_match and recipes[-1-len(digits_to_match):-1] != digits_to_match:
        index0, index1 = next_recipes(recipes, index0, index1)
    if recipes[-len(digits_to_match):] != digits_to_match:
        recipes.pop()
    return len(recipes) - len(digits_to_match)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', default='084601')
    args = parser.parse_args()
    print("Part 1: {}".format(part1Answer(84601)))
    print("Part 2: {}".format(part2Answer(args.n)))

