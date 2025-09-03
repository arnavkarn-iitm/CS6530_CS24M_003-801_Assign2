from Assign2_Part1.firstTenPoints import elliptic_curve_point_addition_and_doubling, log_print


def double_and_add(x1, y1, num, a, p, log_file):
    if x1 is None or y1 is None:  # Point at infinity
        return None, None

    binary_num = bin(num)[2:]
    log_print(log_file, f"\n\nBinary representation of {num}: {binary_num}")

    result_x, result_y = None, None  # Initialize result as point at infinity
    current_p = 0

    for i, bit in enumerate(binary_num):
        log_print(log_file, f"\nd{len(binary_num) - 1 - i} = {bit}")

        # Double the current result if it exists
        if result_x is not None and result_y is not None:
            log_print(log_file, f"Doubling {current_p}P({hex(result_x)}, {hex(result_y)})")
            result_x, result_y = elliptic_curve_point_addition_and_doubling(
                result_x, result_y, result_x, result_y, p, a, log_file)
            current_p *= 2
        else:
            log_print(log_file, "Result is initially point at infinity, no doubling needed.")
        log_print(log_file, f"{current_p}P: ({hex(result_x) if result_x is not None else None}, {hex(result_y) if result_y is not None else None})")
        # If bit is 1, add the base point
        if bit == '1':
            log_print(log_file, f"Since bit is 1\n{current_p}P({hex(result_x) if result_x is not None else None}, {hex(result_y) if result_y is not None else None}) \n+ P({hex(x1)}, {hex(y1)})")
            result_x, result_y = elliptic_curve_point_addition_and_doubling(result_x, result_y, x1, y1, p, a, log_file)
            current_p += 1
            log_print(log_file, f"{current_p}P: ({hex(result_x)}), {hex(result_y)})")

    return result_x, result_y


if __name__ == '__main__':
    '''
    i. Curve Name: secp256k1
    ii. Equation: y^2≡x^3+7(modp)
    iii. Field Prime: p=2^256−2^32−977
    iv. Base Point (G): Defined in SEC 2
    v. Order (n): Large prime (specified in SEC 2)
    vi. Cofactor: 1
    '''
    point_x1 = point_x2 = int("04 79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798"
                              .replace(" ", ""), 16)
    point_y1 = point_y2 = int("483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8"
                              .replace(" ", ""), 16)
    parameter_a = 0
    prime_p = (2**256) - (2**32) - 977

    # Redirect stdout to both console and file
    with open('assign2-part2.txt', 'w') as logfile:
        scalar = [1201, 3966, 4207]
        for s in scalar:
            double_and_add(point_x1, point_y1, s, parameter_a, prime_p, logfile)
