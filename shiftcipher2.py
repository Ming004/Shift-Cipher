#raw = input( " Plz type your words (at least 200 words): ")
#shift = int(input("Enter: "))

def encrypt_check(raw):
    count = len(raw.split())
    if count < 200:
        return "Must be at least 200 words."
    return "valid...."

def encrypt_cipher(raw, shift):
    upper ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower ='abcdefghijklmnopqrstuvwxyz'
    shift_upper=upper[shift:]+upper[0:shift] # we don't use % 26 because we are using the same length of the alphabet
    shift_lower=lower[shift:]+lower[0:shift]
    table = str.maketrans(upper+lower, shift_upper+shift_lower) # translate table
    encrypt_raw = raw.translate(table)
    reraw = encrypt_raw
    return reraw


def decrypt(raw, shift):

    return encrypt_cipher(raw, -shift)

def cal_word_count_of_cipher(raw):
    count = {}
    for i in raw: count[i.lower()] = count.get(i.lower(), 0) + 1 if i.isalpha() else count.get(i, 0)
    return count

