import os
import json
import random
import time

dir = os.path.dirname(os.path.realpath(__file__))

# get primes
with open(dir + '\\primes.json', 'r') as info:
    prime_list = list(json.load(info).values())[0:299]


def getPossiblePrime(n):
#divide by first 400 primes, if n is divisible by the prime or is too big check again
    while True:
        seed = random.randrange(2**(n-1)+1, 2**n-1)
        for prime in prime_list:
            if seed % prime == 0 and prime**2 <= seed:
                break
            else:
                return seed

def miller_rabin_test(seed, iter):
    max_div_by_two = 0
    even = seed - 1
    
    #see how many times we can divide 2 into seed - 1 (seed should be odd)
    while even % 2 == 0:
        even >>= 1
        max_div_by_two += 1
    
    #test to see if number is prime (75% accurate)
    def composite_test(tester):
        if pow(tester, even, seed) == seed - 1:
            return False
        for i in range(max_div_by_two):
            if pow(tester, 2**i * even, seed) == seed - 1:
                return False
        return True
    
    #repeat test iter amount of times to ensure accuracy
    for i in range(iter):
        if composite_test(random.randrange(2, seed)):
            return False
    return True

#get a prime and check with the miller rabin test 20 times
def get_rand_prime(bits: int):
    i = 0
    while True:
        seed = getPossiblePrime(bits)
        if not miller_rabin_test(seed, 20):
            continue
        else:
            return seed

#recursion to find GCD
def gcd_ext(a, b):
    global x, y
 
    # base case
    if (a == 0):
        x = 0
        y = 1
        return b
 
    # store results of recursive call
    gcd = gcd_ext(b % a, a)
    x1 = x
    y1 = y
 
    # update x and y using results of recursive call
    x = y1 - (b // a) * x1
    y = x1
    return gcd
 
# X ~= A^-1 mod M
#calculate modulo inverse
def multi_mod_inverse(A, M):
 
    g = gcd_ext(A, M)
    # m is added to handle negative x
    res = (x % M + M) % M
    return res

dir = os.path.dirname(os.path.realpath(__file__))

print("finding primes, please wait...")

#generate two primes
prime_1 = get_rand_prime(1024)
print('p1 done')
prime_2 = get_rand_prime(1024)
print('p2 done')

#build components of secret key n and phi(n)
n = prime_1 * prime_2
phi_n = (prime_1 - 1)*(prime_2 - 1)

prime_1 <<= 1024
prime_1 += prime_2
#p1 has bit length 2048, holds the secret key

#finds a random number in a smaller pool of known prime numbers to check for coprimes
with open(dir + '\\primes.json', 'r') as info:
    prime_list = list(json.load(info).values())[54:96]
    while True:
        rand_9bit_prime = random.randint(0, len(prime_list) - 1)
        coprime_phi = prime_list[rand_9bit_prime]
        if phi_n % coprime_phi != 0:
            break
print('coprime found')

d = multi_mod_inverse(coprime_phi, phi_n)

#d has bit length of 2047
prime_1 <<= 2048
prime_1 += d
sk = hex(prime_1)

#store coprimes
n <<= 9
n += coprime_phi

#convert to hex add generate or replace json files holding secret and public keys
pk = hex(n)
with open(dir + '\\pk.json', 'w', encoding='utf-8') as keys:
    keys_generated = { "pk" : pk }
    json.dump(keys_generated, keys, ensure_ascii=False, indent=4)
with open(dir + '\\sk.json', 'w', encoding='utf-8') as keys:
    keys_generated = { "sk" : sk }
    json.dump(keys_generated, keys, ensure_ascii=False, indent=4)