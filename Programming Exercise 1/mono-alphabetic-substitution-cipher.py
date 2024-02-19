# Project 0: Mono-Alphabetic Substitution Cipher
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

import hashlib
from tqdm import tqdm
from itertools import permutations


N = 576  # Length of Original Text + It's Hash i.e. 512 + 64 = 576


def encrypt(plain_text, key):

    cipher_text = ""

    for i in range(0, N, 2):
        cipher_text += key[plain_text[i: i + 2]]

    return cipher_text


def decrypt(cipher_text, key):

    plain_text = ""

    for i in range(0, N, 2):
        for k, v in key.items():
            if v == cipher_text[i: i + 2]:
                plain_text += k
                break

    return plain_text


def mapper(hash):

    mapping = ""

    for i in range(64):
        mapping += chr(ord('A') + (ord(hash[i]) - ord('A')) % 3)

    return mapping


def brute_force_attack(cipher_text):

    cnt = 0
    keys = ['AB', 'AC', 'BA', 'BC', 'CA', 'CB', 'AA', 'BB', 'CC']
    all_combinations = list(permutations(keys))

    for combination in tqdm(all_combinations, desc="Brute Force Progress"):
        cnt += 1
        new_key = {keys[i]: combination[i] for i in range(len(keys))}

        decrypted_text = decrypt(cipher_text, new_key)
        if mapper(hashlib.sha256(decrypted_text[:-64].encode()).hexdigest()) == decrypted_text[-64:]:
            return cnt, new_key


if __name__ == "__main__":

    print(" ")

    flag = False
    plain_texts = []
    cipher_texts = []
    decrypted_texts = []
    original_texts = [
        'BCBBBCABCCCBCBBBACBBBBBAAABAABACCABBCCBCAABCBABBACACAAAAAACABCBACACCACABCBCBBCCABABBBBCBCABABABABBABBCCACABBCBAAAAACCBCBABABACCACCBBBABACCABACACBBCAACACABABCBCBBCCCBBBAABBBBBACBCCBACCBCBCBBABBCBACBBACACBCABCACACCAAABAAACCCBCACCBBACCCCBCBCACABABACCACCABACBBCBBCBACBACBBBACAAABABCCCBBAAAACBBABCBBACCBBACBAABCABABAABCBCAAAABAACACCBABBAABBABACBBBCBCBCABCCAACACABCABAABBBCCBABABCBCBBCBCBBBAAAAACBAAAABCCABCBCCCACCBCBBABBAABAACAABBCAAAAABABBCAACABBCBBBACABABABCCABBAAACBBABBBCCCCBBABABCBBCACBBBABBABBBCAABBBBCAACAABAAA',
        'AACACBABCAACCCCABBCBCCCAACAACAAABBAAACCBABBACBAABCBAAAACBCCCCBBBCAABACACCAAABACCCCCCCAAAACBBAAAAABABACBABABCBAABABAAACCAAABAACCACACAAACBBCBBCBCBACCCCBBCBBBCCBBBCCBABBBCABCCBBCBAACBBCCAAABCCABABBACCAABABCCCCCBBCBCBCACABBCAACCACCBBCCCBBBBBCCABCCCABCACACBBABCCABCCAAABBABBCCABAAACCABABBBCAAAACBBCBCBABBCABBACACABBCBAABCBBCBCBBBCACCCBBBCBACABBAABCCAACBCBAAACABBBBACACACCCBCBABCCCCACCCCACBBCAACBCCBCCCCABACCBACAAACCAABCAAACABCABCCCBBBCCAAAACCAACCAAAAAAACBCCAACCCCBBBABAABCCAAAABBCCABBCCACAACBBACCBCACCBBBCACBACCCBCACB',
        'ABBAABACBAAAAACABAABBBACAACACABBAAAACBACBBBBBBCBBCCABBACACAACCCBCABCBBBCBCACACAAABBACCCBCBACBBCCCAACBBACBCABBCCAACACABBABCBCACBBCACACAABBBBCCCAAACCBCCCBAABCABBCCBACABCCCBBAABAABABCBBCBCBAACCABCAAACBABABCACBACACBBAACCABBACCACABBBBABAAAABBAAAABCACCBBBCAACCBAACBACCBCABABBABABACBABABCCACAAAABCBBACCCBCAACABABBCBAAABACAACACAAAABCCCAABAAABAACACBCBBCCBAABABCACACBCBAABCCAABABBBBBABCAACBABBBBACABABABACCAABACCAACBAAAABBCBAABCACACCCBBBCABBBCBAAAABCCCCBCCCAACABBBAAAACCACCBCBACBCCCABCCBBCBBAAACCAABAACBCACCBBBBABBCCCBCACC',
        'CACBCABABCBACCCBABACACCBABABBCBCAACAABBBBCCBCBBCAACBACCCBBAABABCAABCCCCACACABABABBCBBACCACABCBBABABCBABACABAACABCBCCCBBBCCACCABAABCBAACACABABCACACBCCBACACBBACBABCBCACABBCBACABABCBCCCCCBBBCACBBBCCCBAABBBBCAAACCBBCBCBBBCAACBCBAACBABCACCBBCBCCACABCACCAACCCBABBACAABCAAACBACBCACBACBBCCBCCCAAACBCACBBCBCCBBBBCBBCACCCCACCBCABABBABAAAAAACAABBCAABACBABCACABAACBBBBCBACCCCCBAABBAACBCCCBABAACCACCBACBBBBBBCAABCBBACACABBBBCCBCAABBCBCAAACCABBBCACBBBAACACACCBCCACAABBCBABCBACBACACBBCABAAAACCCACCBABABAAACCAACBBBCBAAABCBACACBC',
        'AAABBBBBBAAACCACBCAAACCCBCABCCBAACCCABBAABBCBBACABCCABCCCACAABCACBBBCBAABCCCBBBBBBABCACCCBCCCABACACCACACBCABBBCCACCCACABCAAABCACBBCABCBBCCAAACCCBCAAABABBBBABCBCACBCBBBCBBCAABCCCBAABCBAACCAABBBBCCBACCCAACABCCACCACBCBACCBABABBCCCCBCCBACCAACCABCCAACCABCCAAAABBCCCBBCAAAABAACBABACBAABCCABACCAACBBBABAAACBAABABCACBBCCBCCCAACACACABABBACBABBAACABBCABAACCACAACABAAAACBACABABCACBCBACCACCAAABABBBBBCABCAABACAAACBBBABBCBCBBCAAABABBABAAACCBCCBCBAABCAACABACBCCAABBACBBAAACCAABCAACBCABCAAAACBAAAABAAAABCBBABBABCCCABBBBBBCAAAAB'
    ]

    original_key = {
        'AB': 'CC',
        'AC': 'BB',
        'BA': 'AA',
        'BC': 'CB',
        'CA': 'CA',
        'CB': 'BC',
        'AA': 'BA',
        'BB': 'AC',
        'CC': 'AB'
    }

    for original_text in original_texts:
        plain_texts.append(
            original_text + mapper(hashlib.sha256(original_text.encode()).hexdigest()))

    for plain_text in plain_texts:
        cipher_texts.append(encrypt(plain_text, original_key))

    for cipher_text in cipher_texts:
        decrypted_texts.append(decrypt(cipher_text, original_key))

    for i in range(len(plain_texts)):
        if plain_texts[i] == decrypted_texts[i]:
            print("Plain Text " + str(i + 1) +
                  " Equal to Decrypted Text " + str(i + 1))

        else:
            print("Plain Text " + str(i + 1) +
                  " Not Equal to Decrypted Text " + str(i + 1))

    print("\n\nStarted Brute Force Attack on Cipher Text 1\n")
    cnt, key = brute_force_attack(cipher_texts[0])

    if key is not None:
        print("Key: ", key)
        print("Key Found after " + str(cnt) + " Combinations")

    for i in range(1, len(plain_texts)):
        decrypted_text = decrypt(cipher_texts[i], key)
        if mapper(hashlib.sha256(decrypted_text[:-64].encode()).hexdigest()) != decrypted_text[-64:]:
            flag = False
            print("\nBrute Force Attack Failed\n")
            break

        else:
            flag = True

    if flag:
        print("\nBrute Force Attack Successful on all Cipher Texts\n")
