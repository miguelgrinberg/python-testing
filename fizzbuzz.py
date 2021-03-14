def fizzbuzz(i):
    if i % 15 == 0:
        return "FizzBuzz"
    elif i % 3 == 0:
        return "Fizz"
    elif i % 5 == 0:
        return "Buzz"
    else:
        return i


def main():
    for i in range(1, 101):
        print(fizzbuzz(i))


if __name__ == '__main__':  # pragma: no cover
    main()
