import json
import os

#takes string and converts to a number based on ASCII number formatted as 1XXXXXXXYYYYYYY... where each set of 7 bits = a char's ASCII code
def str_to_num(a: str):
    str_to_bin = 1
    for c in reversed(a):
        str_to_bin <<= 7
        str_to_bin += ord(c)
    return str_to_bin

#inverts the previous operation
def num_to_str(a):
    assert((a.bit_length() - 1) % 7 == 0)
    bin_to_str = a
    str_out = ""
    for i in range(int((a.bit_length() - 1) / 7)):
        str_out += chr(bin_to_str & 127)
        bin_to_str >>= 7
    return str_out

if not os.path.exists("decrypt/sk.json"):
    raise Exception("No key found to encrypt with. Move a .json file named and containing a 'sk' component into the encrypt folder and run the program again.")
if not os.path.exists("decrypt/data.json"):
    raise Exception("No data file found. Move a .json file named 'data.json' into the encrypt folder with a 'encrypted_message' component and run the program again.")

#grab secret key
with open("decrypt/sk.json", 'r') as data:
    key = json.load(data)
sk = key["sk"]

sk = int(sk, 16)

#grab message
with open("decrypt/data.json", 'r') as data:
    f = json.load(data)
enc_msg_list = f["encrypted_message"]

#split secret key into its components
p1p2 = sk >> 2048
p2 = p1p2 & (2**1024 - 1)
p1 = p1p2 >> 1024
n = p1 * p2

d = sk & (2**2048 - 1)
msg = ""
for e in enc_msg_list:
    #reconvert each set of 100 characters and add it to the dict
    c = int(e, 16)
    dec_msg = pow(c, d, n)
    msg += num_to_str(dec_msg)

os.remove('decrypt/data.json')
with open("data.json", 'w', encoding='utf-8') as data:
    out = { "message" : msg }
    json.dump(out, data, ensure_ascii=False, indent=4)