# bobbyRSAEncryption
 My own iteration of RSA encryption for my use and for fun.
 It uses the same modulo arithemetic to create a one-way function as conventional RSA encryption, but compiled in my own way and developed entirely on my own. [^1] [^2]
 As of now, it only converts **string -> hex**. Technically the hex is posed as a string, but is a hexadecimal number containing the encrypted string.
 However, any number of characters can easily and quickly be converted once keys have been generated.
## Usage
 It comes packaged with a **data.json** file, but the **sk.json** and **pk.json** files holding the keys to encrypt and decrypt. Keys made elsewhere generally will not work, only keys produced by the program will work.
 ### Key Generation
 Run **generate_new_keys.py** and, after some time, it will generate a unique public and secret key in their respect files (**pk.json and sk.json** respectively).
 As per usual with RSA, the PK is needed to encrypt **data.json** for exclusive use by the owner of that public key. Using either your newly generated PK for personal use or a PK from a different iteration of keys, put the desired public key file in the **encrypt** folder.
 Similarly, put your desired SK into the **decrypt** folder. It can be any SK, but I recommend keeping your own SK file in the **decrypt** folder.
 ### Encryption and decryption
 Open **data.json** and replace the message string with whatever information you want to encrypt.
 Then, move the folder into the **encrypt** folder and run **encrypt.py**.
 It will return the **data.json** file back to the home directory for distribution encrypted with the given PK in the **encrypt** folder.
 Once encrypted, move **data.json**, into the decrypt folder and, if the SK matches, will return the decrypted message.

 [^1] Important to note I don't know exactly how RSA is professionally and/or conventionally formatted, however the keys generated are equally as strong and usable as it uses the same arithmetic.
 [^2] I did not completely reinvent the algorithims, rather I knew the math on paper and implented in code as made sense to me.
