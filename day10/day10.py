def main():

    adapters: List[int]
    with open('input.txt') as input_file:
        adapters = sorted(list(map(int, input_file.read().split('\n'))))

    # The charging outlet has a rating of 0. We insert at the beginning of the
    # sorted list to preserve its order.
    adapters.insert(0, 0)
    # The device's built-in adapter's rating is always 3 higher than the highest
    # adapter. We append to the end of the sorted list to preserve its order.
    adapters.append(max(adapters) + 3)

    differences_of_1: int = 0
    for i in range(0, len(adapters) - 1):
        if adapters[i+1] - adapters[i] == 1:
            differences_of_1 += 1

    differences_of_3: int = 0
    for i in range(0, len(adapters) - 1):
        if adapters[i+1] - adapters[i] == 3:
            differences_of_3 += 1
            
    print('differences_of_1: ', differences_of_1)
    print('differences_of_3: ', differences_of_3)
    solution_1: int = differences_of_1 * differences_of_3
    s1: str = 'Part 1: The product of the 1-jolt differences and the 3-jolt'\
        f' differences is {solution_1}.'
    print(s1)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(s1)


if __name__ == '__main__':
    main()