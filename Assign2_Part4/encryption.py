import hashlib
import shutil
import subprocess

from Assign2_Part1.firstTenPoints import log_print
from Assign2_Part2.doubleAndAddAlgorithm import double_and_add

if __name__ == '__main__':
    with open('assign2-part4.txt', 'a') as logfile:
        log_print(logfile, f'\nCompiling and running ChaCha20 encryption program:')
        logfile.flush()
        subprocess.run(["g++", "-O2", "-std=c++17", "../CS24M801_chacha20.cpp", "-o", "chacha_encrypt"], stdout=logfile,
                       check=True)

        subprocess.run([
            "./chacha_encrypt",
            "ecd_shared_key.bin",
            "assign2.zip",
            "assign2-encrypted.bin",
            "false"
        ], stdout=logfile)

        shutil.copy("assign2-encrypted.bin", "../Assign2_part5/assign2-encrypted.bin")
        log_print(logfile, f'Encrypted file copied to Assign2_part5 directory for decryption.')
