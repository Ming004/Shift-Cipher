#raw = input( " Plz type your words (at least 200 words): ")
#shift = int(input("Enter: "))

def encrypt_check(raw):
    return "valid" if len(raw.split()) >= 200 else "Text must be at least 200 words"

def encrypt_cipher(raw, shift):
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower = 'abcdefghijklmnopqrstuvwxyz'
    shift_upper = upper[shift % 26:] + upper[:shift % 26]
    shift_lower = lower[shift % 26:] + lower[:shift % 26]
    table = str.maketrans(upper + lower, shift_upper + shift_lower)
    return raw.translate(table)

def decrypt(raw, shift):
    return encrypt_cipher(raw, -shift)

def cal_word_count_of_cipher(raw):
    count = {}
    for i in raw:
        if i.isalpha():
            key = i.lower()
        else:
            key = i
        count[key] = count.get(key, 0) + 1
    return count