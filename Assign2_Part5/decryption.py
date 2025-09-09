import subprocess

if __name__ == '__main__':

    with open('assign2-part5.txt', 'w') as logfile:
        logfile.write(f'\nCompiling and running ChaCha20 decryption program:\n')
        logfile.flush()
        subprocess.run(["g++", "-O2", "-std=c++17", "../CS24M801_chacha20.cpp", "-o", "chacha_decrypt"], stdout=logfile,
                       check=True)

        subprocess.run([
            "./chacha_decrypt",
            "ecd_shared_key.bin",
            "assign2-encrypted.bin",
            "assign2-decrypted.zip",
            "false"
        ], stdout=logfile)

