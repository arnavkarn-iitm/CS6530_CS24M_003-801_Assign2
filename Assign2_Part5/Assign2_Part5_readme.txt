Part 5: ChaCha20 Decryption and Signature Verification

Files:

    1. decryption.py
    2. assign2-part5.txt

How to Run:

    1. Compile and run ChaCha20 decryption:

        python decryption.py

    2. This creates chacha_decrypt.exe and decrypts assign2-encrypted.bin to produce assign2-decrypted.zip.

    3. The process and any logs are saved in assign2-part5.txt.

    4. After decryption, verify assignment signature using your ECDSA signing/verification Python code (if required for peer review).

Notes:

    1. Make sure ecd_shared_key.bin and assign2-encrypted.bin are in the folder before decryption.
    2. The decrypted zip should match the original input for successful decryption.
