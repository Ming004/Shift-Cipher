#raw = input("Plz type your words (at least 200 words): ")
#shift = int(input("Enter: "))

def encrypt_check(raw):
    word_count = len(raw.split())
    if word_count < 200:
        return "Must be at least 200 words."
    return "valid...."

def encrypt_cipher(raw, shift):
    bgEng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smEng = "abcdefghijklmnopqrstuvwxyz"
    shift_smEng = smEng[shift-26:] + smEng[0:(26-shift)]
    shift_bgEng = bgEng[shift-26:] + bgEng[0:(26-shift)]
    encrypt_tx = ""
    for char in raw:
        if char.isupper():
            tx = bgEng.find(char)
            if tx != -1:
                encrypt_tx += shift_bgEng[tx]
            else:
                encrypt_tx += char
        elif char.islower():
            tx = smEng.find(char)
            if tx != -1:
                encrypt_tx += shift_smEng[tx]
            else:
                encrypt_tx += char
        else:
            encrypt_tx += char
    return encrypt_tx

#cipher = input("Paste in here:")

def decrypt(cipher, deshift):
    Eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    decrypt_Eng = Eng[26-deshift:] + Eng[0:(26-deshift)]
    decrypt_tx = ""
    for char in cipher:
        if char.isupper():
            x = decrypt_Eng.find(char)
            if x != -1:
                decrypt_tx += Eng[x]
            else:
                decrypt_tx += char
        elif char.islower():
            x = decrypt_Eng.find(char.upper())
            if x != -1:
                decrypt_tx += Eng[x].lower()
            else:
                decrypt_tx += char
        else:
            decrypt_tx += char
    return decrypt_tx







