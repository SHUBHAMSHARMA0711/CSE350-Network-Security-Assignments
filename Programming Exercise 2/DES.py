# Project 0: DES Implementation
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

initial_permutation_Box = [ 58, 50, 42, 34, 26, 18, 10, 2,
                            60, 52, 44, 36, 28, 20, 12, 4,
                            62, 54, 46, 38, 30, 22, 14, 6,
                            64, 56, 48, 40, 32, 24, 16, 8,
                            57, 49, 41, 33, 25, 17, 9 , 1,
                            59, 51, 43, 35, 27, 19, 11, 3,
                            61, 53, 45, 37, 29, 21, 13, 5,
                            63, 55, 47, 39, 31, 23, 15, 7]


expansion_permutation_Box = [32, 1, 2 , 3 , 4 , 5 , 4 , 5 ,
                            6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
                            12, 13, 12, 13, 14, 15, 16, 17,
                            16, 17, 18, 19, 20, 21, 20, 21,
                            22, 23, 24, 25, 24, 25, 26, 27,
                            28, 29, 28, 29, 30, 31, 32, 1 ]


S_Box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


P_BOX = [16, 7, 20, 21,
        29, 12, 28, 17,
        1 , 15, 23, 26,
        5 , 18, 31, 10,
        2 , 8 , 24, 14,
        32, 27, 3 , 9 ,
        19, 13, 30, 6 ,
        22, 11, 4 , 25]


parity_drop_Box = [ 57, 49, 41, 33, 25, 17, 9 ,
                    1 , 58, 50, 42, 34, 26, 18,
                    10, 2 , 59, 51, 43, 35, 27,
                    19, 11, 3 , 60, 52, 44, 36,
                    63, 55, 47, 39, 31, 23, 15,
                    7 , 62, 54, 46, 38, 30, 22,
                    14, 6 , 61, 53, 45, 37, 29,
                    21, 13, 5 , 28, 20, 12, 4 ]


D_Box = [14, 17, 11, 24, 1 , 5,
        3 , 28, 15, 6 , 21, 10,
        23, 19, 12, 4 , 26, 8 ,
        16, 7 , 27, 20, 13, 2 ,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]


final_permutation_Box = [40, 8, 48, 16, 56, 24, 64,32,
                        39, 7, 47, 15, 55, 23, 63, 31,
                        38, 6, 46, 14, 54, 22, 62, 30,
                        37, 5, 45, 13, 53, 21, 61, 29,
                        36, 4, 44, 12, 52, 20, 60, 28,
                        35, 3, 43, 11, 51, 19, 59, 27,
                        34, 2, 42, 10, 50, 18, 58, 26,
                        33, 1, 41, 9 , 49, 17, 57, 25]


def bin_to_dec(bin_str):

    return int(str(bin_str), 2)


def dec_to_bin(dec_str):

    return bin(int(dec_str))[2:].zfill(4)


def generate_round_keys(left, right, shift):
    
    '''Generate Round Keys by Shifting 
        Left and Right Halves of the Key'''
    
    for i in range(shift):
        nLeft  = ""
        nRight = ""
        for i in range(1, 28):
            nLeft  += left[i]
            nRight += right[i]
       
        left  = nLeft  + left[0]
        right = nRight + right[0]


    '''Combine Left and Right Halves and Apply Permutation'''

    return left, right, "".join([(left + right)[i - 1] for i in D_Box])


def encrypt(left, right, key):

    '''Apply Expansion Permutation and XOR with Key'''

    expansion_result = "".join([right[i - 1] for i in expansion_permutation_Box])
    xor_result = str(bin(int(expansion_result, 2) ^ int(key, 2)))[2:].zfill(48)
    

    '''Apply S-Box Substitution'''

    S_Str = ""
    for i in range(0, 8):
        S_row = xor_result[(i * 6)]     + xor_result[(i * 6) + 5]
        S_col = xor_result[(i * 6) + 1] + xor_result[(i * 6) + 2] + xor_result[(i * 6) + 3] + xor_result[(i * 6) + 4]

        S_Str += dec_to_bin(S_Box[i][bin_to_dec(S_row)][bin_to_dec(S_col)])


    '''Apply Permutation Box and XOR with Left Half'''

    return right, str(bin(int(left, 2) ^ int("".join([S_Str[i - 1] for i in P_BOX]), 2)))[2:].zfill(32)



if __name__ == "__main__":
    plain_texts = ["+C$#W^f5j?v3EQVHA{qA%WS(w.&&?4aUUrK.r3Yc*6vmmx,taU6wzRaFf[rFLfK5Q1Qe$g_=?@dH1PPv",
                   "ReBtyD,!]PaHcn6Gy0_{./YA,6kLRCy?(&/*WrbdGUf,]SfVR&tjhTpap6N]HkrWgXU@?Y{2f?{0fqGQ",
                   "64XvR]L.Q+yck:05N]8MH]XAtbEXvFJ+T2&@N$kRJ0wCZBC?B{d+;Tnu,.+(uM6rY*)tuFnezQyRdD-G",
                   "#z=gV?[(wtX[SNjhB=(J{ZKYBg,!1]dz@c2{qNvb1:V0]T87ZSpySa&.d/%6_nGxMPgaf;{_+(-C)b@i",
                   "&eqw+Cu=QBkA_+Eb4[T$iR9WM$cd2vzEB_mC8-*S+cn((KwkWLu]2v:GY03iUUFru]jp_9:;y0{xFi)!",]
    
    key = "$hk5w^N+"
    
    for text_no, plain_text in enumerate(plain_texts):

        print("\nFor Plain Text " + str(text_no + 1) + ":- \n")

        '''Padding Plain Text to make it Multiple of 64 bits'''

        if len(plain_text) % 16 != 0:
            plain_text += str(16 - len(plain_text) % 16) * (16 - len(plain_text) % 16)
        

        '''Convert Plain Text to Binary'''

        plain_text = "".join(format(ord(i), '08b') for i in plain_text)


        '''Convert Key to Binary and Apply Parity Drop'''

        key = "".join([format(ord(i), '08b') for i in key])
        key = "".join([key[i - 1] for i in parity_drop_Box])


        keys = []
        keyLeftHalf  = key[0  : 28]
        keyRightHalf = key[28 : 56]

        encryption_rounds_result = {}
        decryption_rounds_result = {}

        cipher_text = ""

        '''Iterating over Plain Text in Blocks of 64 bits'''

        for i in range(0, len(plain_text), 64):

            '''Apply Initial Permutation'''

            text = "".join([(plain_text[i : i + 64])[j - 1] for j in initial_permutation_Box])

            left  = text[0  : 32]
            right = text[32 : 64]


            '''Generating Round Keys and Encrypting Plain Text'''

            for i in range(0, 16):
                keyLeftHalf, keyRightHalf, key = generate_round_keys(keyLeftHalf, keyRightHalf, 1 if i in [0, 1, 8, 15] else 2)
                keys.append(key)
                left, right = encrypt(left, right, key)
                
                if i == 0 or i == 13:
                    encryption_rounds_result[i] = [left, right]

            '''Applying Final Permutation'''

            cipher_text += "".join([(right + left)[j - 1] for j in final_permutation_Box])


        print("Cipher Text:- \n" + cipher_text + "\n")

        decrypted_text = ""

        '''Iterating over Cipher Text in Blocks of 64 bits'''

        for i in range(0, len(cipher_text), 64):

            '''Applying Initial Permutation to Cipher Text'''

            text = "".join([cipher_text[i : i + 64][j - 1] for j in initial_permutation_Box])

            left  = text[0  : 32]
            right = text[32 : 64]


            '''Decrypting Cipher Text using Round Keys in Reverse Order'''

            for i in range(0, 16):
                left, right = encrypt(left, right, keys[15 - i])

                if i == 1 or i == 14:
                    decryption_rounds_result[i] = [left, right]


            '''Applying Final Permutation'''

            decrypted_text += "".join([(right + left)[j - 1] for j in final_permutation_Box])
       


        for keyy, value in encryption_rounds_result.items():
            print("Output of Encryption Round " + str(keyy + 1)  +  "  is " + value[0] + value[1])
            print("Output of Decryption Round " + str(15 - keyy) + " is " + decryption_rounds_result[14 if keyy == 0 else 1][1] + decryption_rounds_result[14 if keyy == 0 else 1][0] + "\n")

            if value[0] == decryption_rounds_result[14 if keyy == 0 else 1][1] and value[1] == decryption_rounds_result[14 if keyy == 0 else 1][0]:
                print("Output of Encryption Round " + str(keyy + 1) + " is SAME as Output of Decryption Round " + str(15 - keyy) + "\n\n")

            else:
                print("Output of Encryption Round " + str(keyy + 1) + " is NOT SAME as Output of Decryption Round " + str(15 - keyy))


        if plain_text == decrypted_text:
            print("Encryption and Decryption SUCCESSFUL" + "\n")

        else:
            print("\nEncryption and Decryption FAILED" + "\n")