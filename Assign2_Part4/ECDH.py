import hashlib
import shutil
import subprocess

from Assign2_Part1.firstTenPoints import log_print
from Assign2_Part2.doubleAndAddAlgorithm import double_and_add

if __name__ == '__main__':
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
    peer_public_key = (int("0xABCD"[2:], 16),
                       int("0x0F0F"[2:], 16))  # Peer public key
    private_key = 801  # Private key
    with open('assign2-part4.txt', 'w') as logfile:
        log_print(logfile, f'\nCalculating public key k(B)')
        public_key = double_and_add(x1, y1, private_key, a, p, logfile)
        log_print(logfile, f'\nPublic Key: ({hex(public_key[0])}, {hex(public_key[1])})')
        log_print(logfile, f'\nCalculating common shared secret k(peer_public_key)')
        common_shared_secret = double_and_add(peer_public_key[0], peer_public_key[1], private_key, a, p, logfile)
        log_print(logfile, f'\nCommon Shared Secret: ({hex(common_shared_secret[0])}, {hex(common_shared_secret[1])})')
        log_print(logfile, f'\nUsing x coordinate of common shared secret as '
                           f'symmetric key: {hex(common_shared_secret[0])}')
        chacha_key = hashlib.sha256(common_shared_secret[0].to_bytes(32, byteorder='little')).digest()

        log_print(logfile, f'ChaCha key (SHA-256 of x coordinate): {chacha_key.hex()}')
        # Write key
        with open('ecd_shared_key.bin', 'wb') as key_file:
            key_file.write(chacha_key)
        shutil.copy("ecd_shared_key.bin", "../Assign2_Part5/ecd_shared_key.bin")
        log_print(logfile, f'ChaCha Key copied to Assign2_part5 directory for decryption.')
