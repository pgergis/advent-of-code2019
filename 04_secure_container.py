def hasDouble(n):
    s = str(n)
    for c in list(s):
        if c * 2 in s:
            return True
    return False


def hasStrictDouble(n):
    s = str(n)
    for c in list(s):
        if c * 2 in s and c * 3 not in s:
            return True
    return False


def increasingDigits(n):
    s = str(n)
    return list(s) == sorted(s)


def validPass1(n):
    return hasDouble(n) and increasingDigits(n)


def validPass2(n):
    return hasStrictDouble(n) and increasingDigits(n)


print("q1", len([n for n in range(123257, 647016) if validPass1(n)]))
print("q2", len([n for n in range(123257, 647016) if validPass2(n)]))
