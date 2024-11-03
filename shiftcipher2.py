#raw = input("Plz type your words (at least 200 words): ")
#shift = int(input("Enter: "))

def encrypt_check(raw):
    word_count = len(raw.split())
    if word_count < 200:
        return "Must be at least 200 words."
    return "valid...."

def encrypt_cipher(text, shift):

    shift %= 26
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower = 'abcdefghijklmnopqrstuvwxyz'
    shifted_upper = upper[shift:] + upper[:shift]
    shifted_lower = lower[shift:] + lower[:shift]
    translation_table = str.maketrans(upper + lower, shifted_upper + shifted_lower)
    return text.translate(translation_table)

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
    
    



