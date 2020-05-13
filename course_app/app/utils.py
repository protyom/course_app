import math


def mon_pro(a_, b_, n, k, r_, n_):
    r = 1 << k
    t = a_ * b_
    u = (t + ((t*n_) & (r - 1))*n) >> k
    while u >= n:
        u -= n
    return u


def fast_power(a, e, n):
    k = math.floor(math.log2(n)) + 1
    r = 1 << k
    gcd, r_, n_ = egcd(r, n)
    n_ = -n_
    a_ = (a * r) % n
    x_ = r % n
    while e:
        if e & 1:
            x_ = mon_pro(a_, x_, n, k, r_, n_)
        a_ = mon_pro(a_, a_, n, k, r_, n_)
        e >>= 1

    return x_*r_ % n


def egcd(b, n):
    (x0, x1, y0, y1) = (1, 0, 0, 1)
    while n != 0:
        (q, b, n) = (b // n, n, b % n)
        (x0, x1) = (x1, x0 - q * x1)
        (y0, y1) = (y1, y0 - q * y1)
    return b, x0, y0
