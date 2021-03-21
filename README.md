# safenotes

SafeNotes is an app written in Python that utilizes AES-256 bit encryption technology to securely store notes.

## Encryption

AES-256 bit encryption in AES-CBC mode with 20,000 iterations and PBKDF2 hashing is used to encrypt all data, including metadata. This algorithm and cipher is also used to store the user's decryption key with the user's password.
