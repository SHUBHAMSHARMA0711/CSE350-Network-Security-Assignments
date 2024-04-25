# Project 0: Securely Time-Stamping a Document
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

import os
import rsa
import RSA
import grpc
import PyPDF2
import GMT_pb2
import hashlib
import GMT_pb2_grpc
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_PDF_hash(document):

    all_pages = ""

    with open(document, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page in range(len(reader.pages)):
            all_pages += reader.pages[page].extract_text()

        file.close()

    return hashlib.sha256(all_pages.encode()).hexdigest()


def generate_TXT_hash(document):

    all_content = []

    with open(document, 'r') as file:
        all_content = file.readlines()

        file.close()

    return hashlib.sha256("".join(all_content).encode()).hexdigest()


def generate_PDF(document, signature, timestamp):

    writer = PyPDF2.PdfWriter()

    with open(document, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page in range(len(reader.pages)):
            writer.add_page(reader.pages[page])

        file.close()

    canvass = canvas.Canvas('temp.pdf', pagesize=letter)
    canvass.drawString(100, 100, "GMT Authentication Service")
    canvass.drawString(100, 80, timestamp)
    canvass.drawString(100, 60, signature)
    canvass.save()

    with open('temp.pdf', 'rb') as temp:
        writer.add_page(PyPDF2.PdfReader(temp).pages[0])
        temp.close()

    with open(document, 'wb') as output:
        writer.write(output)
        output.close()

    os.remove('temp.pdf')


def generate_TXT(document, signature, timestamp):

    with open(document, 'a') as file:
        file.write("\nGMT Authentication Service\n" +
                   timestamp + '\n' + signature)
        file.close()


def verify_document(document):

    if document.decode('utf8').endswith(".pdf"):

        all_pages = ""

        with open(document, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in range(len(reader.pages) - 1):
                all_pages += reader.pages[page].extract_text()

            signature = RSA.decrypt(
                server_public_key.e, server_public_key.n, reader.pages[-1].extract_text()[-174:][:-1])

            hash = hashlib.sha256((hashlib.sha256(all_pages.encode()).hexdigest(
            ) + reader.pages[-1].extract_text()[-208:-175][1:]).encode()).hexdigest()

            if hash == signature:
                print("\n\nDocument Timestamped and VERIFIED Successfully.\n\n")

            else:
                print("\n\nDocument Verification Failed.\n\n")

            file.close()

    elif document.decode('utf8').endswith(".txt"):

        lines = []

        with open(document, "r") as file:
            lines = file.readlines()
            file.close()

        content = lines[:-3]
        content[-1] = content[-1][:-1]

        signature = RSA.decrypt(server_public_key.e,
                                server_public_key.n, lines[-1])

        hash = hashlib.sha256((hashlib.sha256(
            "".join(content).encode()).hexdigest() + lines[-2][:-1]).encode()).hexdigest()

        if hash == signature:
            print("\n\nDocument Timestamped and VERIFIED Successfully.\n\n")

        else:
            print("\n\nDocument Verification Failed.\n\n")


if __name__ == '__main__':

    print("\n\n\n<---------------GMT Authentication Service--------------->\n\n\n")

    while True:
        try:
            server_public_key = None
            document = str(
                input("Enter the Document Path or Content: ")).encode()

            channel = grpc.insecure_channel('localhost:50051')
            stub = GMT_pb2_grpc.TimeStampServiceStub(channel)

            with open("GMT_Server_Public_Key.txt", "r") as file:
                lines = file.readlines()
                server_public_key = rsa.key.PublicKey(
                    int(lines[1].split()[1]), int(lines[0].split()[1]))
                file.close()

            if document.decode('utf8').endswith(".pdf"):
                response = stub.GetDocumentTimeStamp(GMT_pb2.TimeStampRequest(document=rsa.encrypt(
                    generate_PDF_hash(document.decode('utf8')).encode(), server_public_key)))

                generate_PDF(document, response.signature, response.timestamp)

            elif document.decode('utf8').endswith(".txt"):
                response = stub.GetDocumentTimeStamp(GMT_pb2.TimeStampRequest(document=rsa.encrypt(
                    generate_TXT_hash(document.decode('utf8')).encode(), server_public_key)))

                generate_TXT(document, response.signature, response.timestamp)

            else:
                response = stub.GetDocumentTimeStamp(GMT_pb2.TimeStampRequest(document=rsa.encrypt(
                    hashlib.sha256(document).hexdigest().encode(), server_public_key)))

                print("\n" + document.decode() + "\nGMT Authentication Service\n" +
                      response.timestamp + '\n' + response.signature)

                signature = RSA.decrypt(server_public_key.e,
                                        server_public_key.n, response.signature)

                hash = hashlib.sha256(
                    (hashlib.sha256(document).hexdigest() + response.timestamp).encode()).hexdigest()

                if hash == signature:
                    print("\n\nDocument Timestamped and VERIFIED Successfully.\n\n")

                else:
                    print("\n\nDocument Verification Failed.\n\n")

                continue

            verify_document(document)

        except KeyboardInterrupt:
            print("\n\n\nGMT Authentication Service Shutting Down...\n\n\n")
            os._exit(0)
