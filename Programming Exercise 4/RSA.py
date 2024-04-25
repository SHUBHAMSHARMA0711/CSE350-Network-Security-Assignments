# Project 0: RSA-based Public-key Certification Authority (CA)
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

from base64 import b64encode, b64decode


def encrypt(e, n, message):

    encrypted_message = ""

    power_raised = pow(int.from_bytes(message.encode("utf-8"), "big"), e, n)

    encrypted_message += b64encode(power_raised.to_bytes(
        power_raised.bit_length() // 8 + 1, "big")).decode("ascii") + " "

    return encrypted_message


def decrypt(d, n, encrypted_message):

    decrypted_message = ""

    for message in encrypted_message.split(" ")[0: -1]:

        power_raised = pow(int.from_bytes(b64decode(message), "big"), d, n)

        decrypted_message += power_raised.to_bytes(
            power_raised.bit_length() // 8 + 1, "big").decode("utf-8")

    return decrypted_message
