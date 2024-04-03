# Project 0: RSA-based Public-key Certification Authority (CA)
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

import os
import sys
import time
import hashlib
from RSA import RSA

import grpc
import CA_pb2
import Client_pb2
import CA_pb2_grpc
import Client_pb2_grpc
from concurrent import futures


class ClientCommunicationServicer(Client_pb2_grpc.ClientCommunicationServicer):

    def __init__(self, rsa, id):

        self.rsa = rsa
        self.CA_public_key = None
        self.client_public_key = None
        self.ids = ["f73d06c9-f15b-4f64-b5ef-ca1cb2c86e3b", "e7f0550e-a5d3-4f63-bd73-f1d5afc28571"]
        self.my_id = self.ids[id - 1]
        self.client_id = self.ids[id % 2]
        self.client_certificate = None
        self.public_key, self.private_key = rsa.generate_key_pair()
        
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = CA_pb2_grpc.CertificateAuthorityStub(self.channel)

        with open ("CA_Public_Key.txt", "r") as file:
            data = file.readlines()
            self.CA_public_key = (int(data[0].split(": ")[1]), int(data[1].split(": ")[1]))

        self.stub.RegisterClient(CA_pb2.ClientInfo(client_id=str(self.my_id), public_key=CA_pb2.Key(e=str(self.public_key[0]), n=str(self.public_key[1]))))


    def request_certificate(self, client_id):

        '''Requesting the certificate from the CA.'''

        response = self.stub.IssueCertificate(CA_pb2.ClientID(id=str(client_id)))

        self.client_certificate = response.certificate
        splitted_certificate = response.certificate.split(" ")

        '''Verifying the certificate and checking its validity. 
            If the certificate is valid, then extracting the public key from the certificate.'''

        if self.verify_certificate(response.certificate) and self.check_validity(response.certificate):
            self.client_public_key = (int(splitted_certificate[6][1]), int(splitted_certificate[7][1 : -3]))

        else:
            print("\nCertificate Verification Failed!\n")

    
    def send_message(self, message):
        
        '''Before sending the message, checking 
            if the Sender has the Receiver's public key or not.'''

        if self.client_public_key == None:
            self.request_certificate(self.client_id)

        '''Checking if the certificate is valid or not.'''

        if not self.check_validity(self.client_certificate):
            print("\nCertificate Expired!")
            print("\nRequesting New Certificate...\n")
            self.request_certificate(self.client_id)

        '''Encrypting the message using RSA and Receiver's public key.'''

        encrypted_message = self.rsa.encrypt(self.client_public_key, message)

        channel = grpc.insecure_channel('localhost:50052' if self.my_id == "e7f0550e-a5d3-4f63-bd73-f1d5afc28571" else 'localhost:50053')
        stub = Client_pb2_grpc.ClientCommunicationStub(channel)

        '''Returning the Acknowledgement received from the Receiver.'''

        return stub.ReceiveMessage(Client_pb2.Message(message=encrypted_message))
    

    def ReceiveMessage(self, request, context):

        '''Decrypting the message using the Receiver's private key.'''

        decrypted_message = self.rsa.decrypt(self.private_key, request.message)

        print(f"\n\nDecrypted Message Using Receiver's PRIVATE KEY")
        print(f"Message: {decrypted_message}\n")
        print("\nEnter Message: ", end=" ")

        '''Before sending the Acknowledgement, checking
            if the Receiver has the Sender's public key or not.'''

        if self.client_public_key == None:
            self.request_certificate(self.client_id)

        '''Sending the Acknowledgement to the Sender.'''

        return Client_pb2.Acknowledgement(acknowledgement=self.rsa.encrypt(self.client_public_key, f"ACK + {decrypted_message}"))


    def verify_certificate(self, certificate):

        '''Verifying the certificate by checking the hash of the certificate data
            and comparing it with the decrypted hash from the certificate.'''

        if hashlib.sha256((" ".join(certificate.split(" ")[0 : -2]) + " ").encode()).hexdigest() == self.rsa.decrypt(self.CA_public_key, certificate.split(" ")[-2] + " "):
            return True
       
        return False
    

    def check_validity(self, certificate):

        '''Checking the validity of the certificate by 
            comparing the current time with the time mentioned in the certificate 
                and checking if the certificate has expired or not.'''

        current_time = int(time.time())
        duration = int(certificate.split("DURATION: ")[1].split(" ")[0])
        certificate_time = int(certificate.split("TIME: ")[1].split(",")[0])

        if current_time - certificate_time < duration:
            return True

        return False
    

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("\n\nUsage: python Client.py <YOUR_ID> <CLIENT_YOU_WANT_TO_SEND_MESSAGE_ID>\n\n")
        os._exit(1)

    rsa = RSA(1024)
    client = ClientCommunicationServicer(rsa, int(sys.argv[1]))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Client_pb2_grpc.add_ClientCommunicationServicer_to_server(client, server)
    server.add_insecure_port('[::]:50052' if sys.argv[1] == "1" else '[::]:50053')
    server.start()

    print("\n\n\nClient Interface Running...\n\n")

    while True:
        try:
            message = str(input("\nEnter Message: "))

            '''Sending the message to the Receiver and 
                then printing the Acknowledgement after decrypting it using the Sender's private key.'''

            print("\nAcknowledgement from Client: ", rsa.decrypt(client.private_key, client.send_message(message).acknowledgement))

        except KeyboardInterrupt:
            print("\n\n\nShutting Down Client Interface...\n\n\n")
            server.stop(0)
            os._exit(0)
