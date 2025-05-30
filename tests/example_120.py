def is_prime(n):
    return all(n % i != 0 for i in range(2, int(n**0.5)+1)) if n > 1 else False
print(is_prime(7))