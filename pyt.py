#!/usr/bin/python3
def factorize(number):
  
    if number < 1:
        raise ValueError("Number must be a positive integer.")

    factors = []
    divisor = 2

    while number > 1:
        while number % divisor == 0:
            factors.append(divisor)
            number //= divisor

        divisor += 1

    return factors


number = int(input("Enter a positive integer: "))
print(factorize(number))


