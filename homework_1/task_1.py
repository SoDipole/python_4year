def fibonacci(n):
    i = 2
    sequence = [0,1]
    while i < n:
        sequence.append(sequence[i-2] + sequence[i-1])
        i += 1
    return sequence[n-1]

for k in range(1,15):
    print(fibonacci(k))
