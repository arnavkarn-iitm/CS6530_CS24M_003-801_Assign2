def log_print(file, *args, **kwargs):
    print(*args, **kwargs, file=file)
    # Optionally also print to console:
    print(*args, **kwargs)


def calculate_s(x1, y1, x2, y2, p, a, log_file):
    if x1 is None or y1 is None:  # Point at infinity
        return None
    if x2 is None or y2 is None:  # Point at infinity
        return None
    if (x1 == x2) and (y1 == y2):  # Point doubling
        log_print(log_file, "Point Doubling")
        numerator = (3 * x1**2 + a) % p
        denominator = (2 * y1) % p
        s = (numerator * pow(denominator, -1, p)) % p  # Modular division
    else:  # Point addition
        log_print(log_file, "Point Addition")
        numerator = (y2 - y1) % p
        denominator = (x2 - x1) % p
        s = (numerator * pow(denominator, -1, p)) % p  # Modular division
    log_print(log_file, f"s: {s}")
    return s


def elliptic_curve_point_addition_and_doubling(x1, y1, x2, y2, p, a, log_file):
    if x1 is None or y1 is None:  # P1 is the point at infinity
        return x2, y2
    if x2 is None or y2 is None:  # P2 is the point at infinity
        return x1, y1
    if x1 == x2 and (y1 + y2) % p == 0:  # P1 + P2 = Point at infinity
        return None, None

    s = calculate_s(x1, y1, x2, y2, p, a, log_file)
    if s is None:  # Handle division by zero or invalid cases
        return None, None

    x = (s**2 - x1 - x2) % p
    y = (s * (x1 - x) - y1) % p
    return x, y


if __name__ == '__main__':
    '''
    i. Curve Name: secp256k1
    ii. Equation: y^2≡x^3+7(modp)
    iii. Field Prime: p=2^256−2^32−977
    iv. Base Point (G): Defined in SEC 2
    v. Order (n): Large prime (specified in SEC 2)
    vi. Cofactor: 1
    '''
    point_x1 = point_x2 = int("79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798"
                              .replace(" ", ""), 16)
    point_y1 = point_y2 = int("483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8"
                              .replace(" ", ""), 16)
    parameter_a = 0
    prime_p = (2**256) - (2**32) - 977

    # Redirect stdout to both console and file
    with open('assign2-part1.txt', 'w') as logfile:
        log_print(logfile, f"Curve parameter a: {parameter_a}")
        log_print(logfile, f"Prime p: {prime_p}")
        current_x1, current_y1 = point_x1, point_y1  # Avoid shadowing
        log_print(logfile, f"Point P: ({hex(current_x1) if current_x1 is not None else 'Infinity'}, "
                           f"{hex(current_y1) if current_y1 is not None else 'Infinity'})")

        for i in range(9):
            log_print(logfile, f"\nPoint {i + 2}P = {str(i+1) if i > 0 else ''}P + P")
            log_print(logfile, f"{str(i+1) if i > 0 else ''}P: ({hex(current_x1) if current_x1 is not None else 'Infinity'}, "
                               f"{hex(current_y1) if current_y1 is not None else 'Infinity'})")
            log_print(logfile, f"+P: ({hex(point_x2) if point_x2 is not None else 'Infinity'}, "
                               f"{hex(point_y2) if point_y2 is not None else 'Infinity'})")
            x3, y3 = elliptic_curve_point_addition_and_doubling(current_x1, current_y1, point_x2, point_y2,
                                                                prime_p, parameter_a, logfile)
            log_print(logfile, f"Point {i+2}P: ({hex(x3) if x3 is not None else 'Infinity'}, "
                               f"{hex(y3) if y3 is not None else 'Infinity'})")
            current_x1, current_y1 = x3, y3
