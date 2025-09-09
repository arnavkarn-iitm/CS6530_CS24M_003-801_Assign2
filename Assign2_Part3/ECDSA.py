import hashlib

from Assign2_Part1.firstTenPoints import log_print, elliptic_curve_point_addition_and_doubling
from Assign2_Part2.doubleAndAddAlgorithm import double_and_add


def combine_files(file_1, file_2, outputfile):
    with open(file_1, 'r') as f1, open(file_2, 'r') as f2, open(outputfile, 'w') as out:
        # Read contents of both files
        content1 = f1.read()
        content2 = f2.read()

        # Write combined content to the output file
        out.write(content1)
        out.write("\n")  # Add a newline between the contents
        out.write(content2)


def generate_hash_as_number(m, order_n):
    # Compute the SHA-256 hash of the message
    hash_bytes = hashlib.sha256(m.encode()).digest()

    # Convert the hash to an integer
    hash_int = int.from_bytes(hash_bytes, byteorder='big')

    # Ensure the hash is in the range [0, order_n - 1]
    hash_value = hash_int % order_n
    return hash_value


def signature_generation(point_x1, point_y1, k, parameter_a, prime_p, log_file, order_n, h, d):
    log_print(log_file, f"\nGenerating Point kG: ")
    kG = double_and_add(point_x1, point_y1, k, parameter_a, prime_p, log_file)

    log_print(log_file, f"\nPoint kG: ({hex(kG[0])}, {hex(kG[1])})")
    # compute r = point_x1 mod n
    r = kG[0] % order_n

    # compute s = k^(-1) * (h + d * r) mod n
    k_inv = pow(k, -1, order_n)  # Modular inverse of k mod n
    s = (k_inv * (h + d * r)) % order_n
    log_print(log_file, f"\nSignature (r, s): ({hex(r)}, {hex(s)})")
    return r, s


def signature_verification(parameter_a, prime_p, log_file, order_n, h, signature, base_x1, base_y1, public):
    s = signature[1]
    r = signature[0]
    w = pow(s, -1, order_n)
    u = (h * w) % order_n
    v = (r * w) % order_n

    log_print(log_file, f"\n\nCalculating vP")
    public_x1 = public[0]
    public_y1 = public[1]
    vP = double_and_add(public_x1, public_y1, v, parameter_a, prime_p, log_file)

    log_print(log_file, f"\n\nCalculating uG")
    uG = double_and_add(base_x1, base_y1, u, parameter_a, prime_p, log_file)

    log_print(log_file, f"\n\nCalculating uG + vP")
    uG_plus_vP = elliptic_curve_point_addition_and_doubling(uG[0], uG[1], vP[0], vP[1], prime_p, parameter_a, log_file)

    log_print(log_file, f"uG + vP: ({hex(uG_plus_vP[0])}, {hex(uG_plus_vP[1])})")
    if (uG_plus_vP[0] % order_n) == r:
        log_print(log_file, "Signature is valid.")
        return True
    else:
        log_print(log_file, "Signature is invalid.")
        return False


if __name__ == '__main__':
    # Combine logs from assign2-part1.txt and assign2-part2.txt
    # File paths
    file1 = '../Assign2_Part1/assign2-part1.txt'
    file2 = '../Assign2_Part2/assign2-part2.txt'
    output_file = 'assign2-part1-part2-combined_logs.txt'

    # Combine the files
    combine_files(file1, file2, output_file)

    '''
    i. Curve Name: secp256r1
    iii. Field Prime: p=2^224(2^32 − 1) + 2^192 + 2^96 − 1
    iv. Base Point (G): Defined in SEC 2
    v. Order (n): Large prime (specified in SEC 2)
    vi. Cofactor: 1
    '''

    x1 = int("6B17D1F2 E12C4247 F8BCE6E5 63A440F2 77037D81 2DEB33A0 F4A13945 D898C296".replace(" ", ""), 16)
    y1 = int("4FE342E2 FE1A7F9B 8EE7EB4A 7C0F9E16 2BCE3357 6B315ECE CBB64068 37BF51F5".replace(" ", ""), 16)
    a = int("FFFFFFFF 00000001 00000000 00000000 00000000 FFFFFFFF FFFFFFFF FFFFFFFC".replace(" ", ""), 16)
    p = (2**224 * (2**32 - 1)) + 2**192 + 2**96 - 1
    n = int("FFFFFFFF 00000000 FFFFFFFF FFFFFFFF BCE6FAAD A7179E84 F3B9CAC2 FC632551".replace(" ", ""), 16)

    d = 801  # Private key
    # Read the combined file as the message
    with open(output_file, 'r') as f:
        message = f.read()
    with open('assign2-part3.txt', 'w') as logfile:
        # Generate the hash value
        hash_value = generate_hash_as_number(message, n)
        log_print(logfile, f"Hash value (h): {hash_value}")

        log_print(logfile, f"\nGenerating Public Key dG: ")
        public_key = double_and_add(x1, y1, d, a, p, logfile)
        log_print(logfile, f"\nPublic Key (dG): ({hex(public_key[0])}, {hex(public_key[1])})")
        log_print(logfile, f"\nGenerating Signature:")
        sign = signature_generation(x1, y1, 123, a, p, logfile, n, hash_value, d)
        log_print(logfile, f"\nVerifying Signature:")
        signature_verification(a, p, logfile, n, hash_value, sign, x1, y1, public_key)

