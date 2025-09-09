Part 4: ECDH Key Agreement and ChaCha20 Encryption

Files:
    1. ECDH.py
    2. encryption.py
    3. assign2-part4.txt

How to Run:

    1. Generate the ECDH key and prepare ChaCha key & logs:

        python ECDH.py

    This creates chacha_encrypt.exe, ecd_shared_key.bin and logs in assign2-part4.txt.

    2. Compile and run ChaCha20 encryption (if not already present):

        python encryption.py

    This compiles chacha_encrypt.exe, encrypts Assign2.zip using the generated key, and writes to assign2-encrypted.bin.

Notes:

    1. All output and compilation details are in assign2-part4.txt.
    2. Verify the existence of Assign2.zip before running encryption.
