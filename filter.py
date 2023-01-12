with open('train.txt', 'r') as f:
    count = 0
    wrong = 0
    for line in f:
        count += 1
        s = line.count(' ')
        if s > 1:
            wrong += 1
            print(line)
    print(count)
    print(wrong)