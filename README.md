# safenotes

SafeNotes is an app written in Python that utilizes AES-256 bit encryption technology to securely store notes.

## Encryption

AES-256 bit encryption in AES-CBC mode with 20,000 iterations and PBKDF2 hashing is used to encrypt all data, including metadata, like note creation dates and times. This algorithm and cipher is also used to store the user's decryption key with the user's password.

## Running

Install the requirements using requirements.txt using `pip install -r requirements.txt`.

You may need to install tkinter if your Python installation did not come pre-installed with it.

After the requirements are installed and you are sure that tkinter is installed, run it using `python safenotes.py`.
