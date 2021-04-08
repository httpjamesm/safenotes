# safenotes

SafeNotes is an app written in Python that utilizes strong encryption technology to securely store notes.

## Features

### Simple

SafeNotes is a simple note-taking app with minimal bloat. It takes only a few seconds to create and save a new note.

### Encryption

AES-256 bit encryption isn't just the default, it's a requirement. No data is stored unencrypted--ever.

### Attachments

Notes support unlimited encrypted attachments, so you can keep track of all types of files within your safe note. 

## Security

### Encryption

AES-256 bit encryption in AES-CBC mode with 20,000 iterations and PBKDF2 hashing is used to encrypt all data, including note attachments and metadata, like note creation dates and times. This algorithm and cipher is also used to store the user's decryption key with the user's password at rest, ensuring that the password cannot be accessed even with physical access to the app's data.

### Local-Only

SafeNotes only keeps data offline, within its folder, and does not require any internet access at all. This significantly decreases the attack surface as no data, encrypted or not, leaves the user's machine.

### On-demand Re-encryption

SafeNotes has the perfect feature for tinfoil hats. If you have a suspicion that your device was somehow compromised, you can re-encrypt your data with just a few clicks. All data will be decrypted in memory, re-encrypted in memory, and written to disk.

## Running

Install the requirements using requirements.txt using `pip install -r requirements.txt`.

You may need to install tkinter if your Python installation did not come pre-installed with it.

After the requirements are installed and you are sure that tkinter is installed, run it using `python safenotes.py`.
