

def fast_power(base, power, mod):
    result = 1
    while power > 0:

        if power % 2 == 1:
            result = (result * base) % mod

        power = power // 2

        base = (base * base) % mod

    return result


def egcd(b, n):
    (x0, x1, y0, y1) = (1, 0, 0, 1)
    while n != 0:
        (q, b, n) = (b // n, n, b % n)
        (x0, x1) = (x1, x0 - q * x1)
        (y0, y1) = (y1, y0 - q * y1)
    return b, x0, y0
