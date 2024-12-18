#raw = input("Plz type your words (at least 200 words): ")
#shift = int(input("Enter: "))

def encrypt_check(raw):
    word_count = len(raw.split())
    if word_count < 200:
        return "Must be at least 200 words."
    return "valid...."

def encrypt_cipher(raw, shift):
    upper ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower ='abcdefghijklmnopqrstuvwxyz'
    shift_upper=upper[shift:]+upper[0:shift] # we don't use % 26 because we are using the same length of the alphabet
    shift_lower=lower[shift:]+lower[0:shift]
    table = str.maketrans(upper+lower, shift_upper+shift_lower) # translate table
    encrypt_raw = raw.translate(table)
    reraw = encrypt_raw + encrypt_raw
    return reraw

def decrypt(text, shift):

    return encrypt_cipher(text, -shift)

def cal_word_count_of_cipher(text):
    freq = {}
    for i in text:
        if i.isalpha():
            i = i.lower()
            freq[i] = freq.get(i, 0) + 1
        return freq 

def cal_k_value(shift):
    
    



