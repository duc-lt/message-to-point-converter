from core.int_operations import is_coprime, is_odd_prime, to_base_2


def inverse(a, mod):
    # thuật toán Euclid mở rộng
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    if not isinstance(a, int) or not isinstance(mod, int):
        return
    if not is_coprime(a, mod):
        return
    r0, r1, r2, s0, s1, s2 = a, mod, 1, 1, 0, 1

    while True:
        q = r0 // r1
        r2 = r0 % r1
        if r2 == 0:
            return s2 % mod
        s2 = s0 - q * s1
        r0, r1, s0, s1 = r1, r2, s1, s2


def add(a, b, mod):
    return (a + b) % mod


def subtract(a, b, mod):
    return (a - b) % mod


def multiply(a, b, mod):
    return (a * b) % mod


def divide(a, b, mod):
    return (a * inverse(b, mod)) % mod


def power(a, b, mod):
    if b == 0:
        return 1
    if b % 2 == 1:
        return multiply(a, power(a * a, (b - 1) / 2, mod), mod)
    return power(a * a, b / 2, mod)


def is_square(a, mod):
    # tiêu chuẩn Euler (Euler's criterion)
    # https://en.wikipedia.org/wiki/Euler%27s_criterion
    return (a % mod == 0) or (is_odd_prime(mod) and power(a, (mod - 1) / 2, mod) == 1)


def find_least_non_residue(mod):
    # tìm z nhỏ nhất sao cho z^((mod - 1) / 2) % mod = mod - 1
    z = 2
    while power(z, (mod - 1) / 2, mod) != mod - 1:
        z += 1
    return z


def square_root(a, mod):
    # thuật toán Tonelli-Shanks
    # https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm
    if is_square(a, mod):
        q, s = to_base_2(mod - 1)
        z = find_least_non_residue(mod)
        m = s
        c = power(z, q, mod)
        t = power(a, q, mod)
        r = power(a, (q + 1) / 2, mod)

        if t == 0:
            return 0

        while t != 1:
            i = 1
            while power(t, 2 ** i, mod) != 1:
                i += 1

            b = power(c, 2 ** (m - i - 1), mod)
            m = i
            c = power(b, 2, mod)
            t = multiply(t, c, mod)
            r = multiply(r, b, mod)

        return r
    return
