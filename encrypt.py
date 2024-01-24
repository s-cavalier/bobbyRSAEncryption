import os
import json

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

#check for necessary files
if not os.path.exists("encrypt/pk.json"):
    raise Exception("No key found to encrypt with. Move a .json file named and containing a 'pk' component into the encrypt folder and run the program again.")
if not os.path.exists("encrypt/data.json"):
    raise Exception("No data file found. Move a .json file named 'data.json' into the encrypt folder with a 'message' component and run the program again.")

#grab public key and split it into its components
with open("encrypt/pk.json", 'r') as data:
    key = json.load(data)
pk = key["pk"]

e = int(pk, 16) & 511
n = int(pk, 16) >> 9

#grabs message
with open("encrypt/data.json", 'r', encoding='utf-8') as data:
    message = json.load(data)
encrypt = message["message"]

#turn message into list of 100 messages so the message length (when converted to num) is never bigger than n
was_100 = False
to_json = []
if len(encrypt) <= 100:
    #basic encrpytion process
    #save string to a num and encrypt that num using public key components
    to_json.append(str_to_num(encrypt))
    to_json[0] = hex(pow(to_json[0], e, n))
    was_100 = True

# if we have a large than 100 string, we repeat the above process for each set of 100 characters
message_list = []
while len(encrypt) > 100:
    message_list.append(encrypt[0:100])
    encrypt = encrypt[100:]
if len(encrypt) <= 100 and not was_100:
    message_list.append(encrypt[0:])

encrypted_message_list = []
for i in range(len(message_list)):
    encrypted_message_list.append(str_to_num(message_list[i]))
    encrypted_message_list[i] = pow(encrypted_message_list[i], e, n)    

#add to dict
for e in encrypted_message_list:
    to_json.append(hex(e))

os.remove('encrypt/data.json')
with open("data.json", 'w', encoding='utf-8') as data:
    enc_msg = { "encrypted_message" : to_json }
    json.dump(enc_msg, data, ensure_ascii=False, indent=4)