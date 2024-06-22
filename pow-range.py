#!/usr/bin/env python

import click


def prime_factors(n):
    i = 2
    factors = {}
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
        i += 1
    if n > 1:
        factors[n] = 1
    return factors


def gcd(*args):
    if len(args) == 1:
        return args[0]
    if len(args) == 2:
        a, b = args
        while b:
            a, b = b, a % b
        return a
    return gcd(args[0], gcd(*args[1:]))


def infer_pow(start, end):
    if end % start:
        raise ValueError(f'{end} is not divisible by {start}')
    quot = end // start
    quot_factors = prime_factors(quot)
    pow_gcd = gcd(*quot_factors.values())
    pow = 1
    for prime, count in quot_factors.items():
        pow *= prime ** (count // pow_gcd)
    return pow


@click.command()
@click.option('-x', '--exclusive-end', is_flag=True, help='Exclude the end value (e.g. interpret range as half-open range)')
@click.argument('arg')
def main(exclusive_end, arg):
    pcs = arg.split(':')
    reverse = False
    if len(pcs) == 1:
        start = 1
        end = int(pcs[0])
        pow = infer_pow(start, end)
    elif len(pcs) == 2:
        start, end = pcs
        start = start or 1
        end = end or 1
        start, end = int(start), int(end)
        if start > end:
            reverse = True
            start, end = end, start
        pow = infer_pow(start, end)
    elif len(pcs) == 3:
        start, end, pow = pcs
        start = start or 1
        end = end or 1
        start, end, pow = int(start), int(end), int(pow)
    else:
        raise ValueError(f'Unrecognized argument: {arg}')

    pows = []
    n = start
    while n <= end:
        pows.append(n)
        if n == end:
            break
        n *= pow
    if n != end:
        raise ValueError(f'Failed to reach {end} from {start} by powers of {pow}')
    if reverse:
        pows = pows[::-1]
    if exclusive_end:
        pows.pop()
    for n in pows:
        print(n)


if __name__ == '__main__':
    main()
