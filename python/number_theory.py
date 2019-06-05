import random
import time

# Reduces the power by taking modulo every iteration. Log(exp) runtime.
def power_mod(num, exp, mod) : 
    ans = 1
    num = num % mod 
    while exp > 0: 
        # Check if exp is odd. If it is mutiply num one time to ans.
        if (exp & 1) == 1: 
            ans = (ans * num) % mod
        # Divide exp by 2
        exp = exp >> 1 
        num = (num * num) % mod 
    return ans

# Factors all the 2's from num
def div_2(num):
    count = 0
    # Check if even. If even divide by 2
    while (num & 1) == 0:
        num = num >> 1
        count = count + 1
    return {'number': num, 'count': count}

# Check if number is probably prime
def miller_rabin_test(number, repeat): 
    # Factor all 2's from number-1. (number-1) would be the order of
    # unit group mod number, if number were prime.
    div_result = div_2(number-1)
    r_power = div_result['count']
    d_number = div_result['number']
    # Will repeat the miller-rabin test with pseudorandom numbers 
    # between 2 and number.
    for count in range(repeat):
        check_int = random.randrange(2, number)
        check = power_mod(check_int, d_number, number)
        mainloop = True
        if (check == 1) or (check == number-1):
            continue
        for innner_count in range(r_power):
            check = power_mod(check, 2, number)
            if check == number-1:
                mainloop = False
                break
        if mainloop:
            return False
    return True

# This is an implementaion of binary gcd recursively
def fast_gcd(num1, num2):
    # If the numbers are the same then GCD is either number
    if num1 == num2:
        return num1
    # If either of the numbers is 0, any number divides 0,
    # so just return the other number.
    elif num1 == 0:
        return num2
    elif num2 == 0:
        return num1
    # If num1 is even and num 2 is odd gcd(num1,num2)=gcd((num1)/2,num2)
    # else if num1 is even and num 2 is also even gcd(num1,num2)=
    # 2*gcd((num1)/2,(num2)/2)
    elif (num1 & 1) == 0:
        if (num2 & 1) == 1:
            return fast_gcd(num1 >> 1, num2)
        else:
            return fast_gcd(num1 >> 1, num2 >> 1) << 1
    # If num1 is odd and num2 is even gcd(num1,num2)=gcd(num1,(num2)/2)
    elif (num2 & 1) == 0:
        return fast_gcd(num1, num2 >> 1)
    # If num1 and num2 are odd and num1 > num2 then 
    # gcd(num1,num2)=gcd((num1-num2)/2, num2)
    elif num1 > num2:
        return fast_gcd((num1-num2) >> 1, num2)
    else:
        return fast_gcd((num2-num1) >> 1, num1)

# Implementation of binary gcd iteratively
def iter_fast_gcd(num1, num2):
    shift = 0
    if num1 == 0:
        return num2
    elif num2 == 0:
        return num1
    else:
        while ((num1|num2) & 1) == 0:
            shift += 1
            num1 >>= 1
            num2 >>= 1
        while (num1 & 1) == 0:
            num1 >>= 1
        while True:
            while (num2 & 1) == 0:
                num2 >>= 1
            if num1 > num2:
                temp = num1
                num1 = num2
                num2 = temp
            num2 -= num1
            if num2 == 0:
                break
    return num1 << shift

def fast_lcm(num1, num2):
    gcd = iter_fast_gcd(num1,num2)
    return (num1*num2) // gcd

def generate_probable_prime(bits):
    # Generate a pseudoprime of 'bits' bits
    rand_int = random.getrandbits(bits)
    start_time = time.time()
    # Increment until we find prime
    while True:
        if (rand_int & 1) == 0:
            rand_int = rand_int + 1
        # Check if probable prime
        elif miller_rabin_test(rand_int, 11):
            break
        # If it takes more then 10 seconds to find a probable prime
        # run the funtion again.
        elif (time.time() - start_time) > 10:
            rand_int = generate_probable_prime(bits)
        else:
            rand_int = rand_int + 2
    return rand_int

# Iterative version of extended gcd to find inverse
def mod_inverse(num, mod_temp) : 
	mod = mod_temp
	y = 0
	x = 1
	if (mod == 1) : 
		return 0
	while (num > 1) :  
		q = num // mod_temp
		t = mod_temp
		mod_temp = num % mod_temp
		num = t 
		t = y 
		y = x - q * y 
		x = t 
	if (x < 0) : 
		x = x + mod
	return x 
