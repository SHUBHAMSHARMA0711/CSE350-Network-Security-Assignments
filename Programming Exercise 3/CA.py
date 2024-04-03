# Project 0: RSA-based Public-key Certification Authority (CA)
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

import os
import time
import uuid
import hashlib
from RSA import RSA

import grpc
import CA_pb2
import CA_pb2_grpc
from concurrent import futures


class CertificateAuthorityServicer(CA_pb2_grpc.CertificateAuthorityServicer):

    def __init__(self, rsa):

        self.rsa = rsa
        self.id = uuid.uuid4()
        self.clients_public_keys = {}
        self.public_key, self.private_key = rsa.generate_key_pair()

        with open("CA_Public_Key.txt", "w") as file:
            file.write(f"e: {self.public_key[0]}\nn: {self.public_key[1]}")


    def RegisterClient(self, request, context):

        self.clients_public_keys[request.client_id] = request.public_key
        
        return CA_pb2.RegistrationResponse(success=True, message=f"Client: {request.client_id}, Registered Successfully.")
    

    def IssueCertificate(self, request, context):

        client_id = request.id

        '''Checking if the client is registered 
            with the CA or not. If registered, then issue the certificate.'''

        if client_id in self.clients_public_keys:

            public_key = self.clients_public_keys[client_id]
            current_time = int(time.time())

            '''Creating the certificate data and then calculating
                the hash of the certificate data and encrypting it using 
                    the CA's private key. After that, appending the encrypted hash to the certificate data.'''

            certificate_data = f"ID_CA: {self.id}, ID_CLIENT: {client_id}, PU_CLIENT: {public_key}, TIME: {current_time}, DURATION: 3600 "
            certificate = certificate_data + self.rsa.encrypt(self.private_key, hashlib.sha256(certificate_data.encode()).hexdigest())
            
            return CA_pb2.Certificate(certificate=certificate)
        
        else:
            return CA_pb2.Certificate(certificate="Client not Found!")


if __name__ == '__main__':

    rsa = RSA(1024)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CA_pb2_grpc.add_CertificateAuthorityServicer_to_server(CertificateAuthorityServicer(rsa), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    print("\n\n\nCertificate Authority Server Running...\n\n\n")
    
    try:
        while True:
            time.sleep(86400)

    except KeyboardInterrupt:
        print("\n\n\nShutting Down Certificate Authority Server...\n\n\n")
        server.stop(0)
        os._exit(0)
