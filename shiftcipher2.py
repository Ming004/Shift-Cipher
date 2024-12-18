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
    result = []
    for char in text:
        if char.isupper():
            index = (upper.index(char) + shift) % 26
            result.append(upper[index])
        elif char.islower():
            index = (lower.index(char) + shift) % 26
            result.append(lower[index])
        else:
            result.append(char)
    return ''.join(result)

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
    
    



