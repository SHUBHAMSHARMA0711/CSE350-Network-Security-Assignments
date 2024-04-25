# Project 0: Securely Time-Stamping a Document
# Contributors: Shubham Sharma (2021099), Parveen (2021079)

import os
import rsa
import RSA
import time
import grpc
import hashlib
import GMT_pb2
import GMT_pb2_grpc
import GMTTimeServer
from concurrent import futures


class TimeStampServiceServicer(GMT_pb2_grpc.TimeStampServiceServicer):

    def __init__(self):

        self.document = None
        self.public_key, self.private_key = rsa.newkeys(1024)

        with open("GMT_Server_Public_Key.txt", "w") as file:
            file.write(f"e: {self.public_key.e}\nn: {self.public_key.n}\n")
            file.close()

    def GetDocumentTimeStamp(self, request, context):

        timestamp = str(GMTTimeServer.get_current_gmt_time())

        self.document = rsa.decrypt(
            request.document, self.private_key).decode('utf-8')

        signature = RSA.encrypt(self.private_key.d, self.private_key.n, hashlib.sha256(
            (self.document + timestamp).encode()).hexdigest())

        print("\n\nDocument Signed and Timestamped Successfully.\n\n")

        return GMT_pb2.TimeStampResponse(signature=signature, timestamp=timestamp)


if __name__ == '__main__':

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    GMT_pb2_grpc.add_TimeStampServiceServicer_to_server(
        TimeStampServiceServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()

    print("\n\n\nGMT Time Stamping Server Running...\n\n\n")

    try:
        while True:
            time.sleep(86400)

    except KeyboardInterrupt:
        print("\n\n\nShutting down GMT Time Stamping Server...\n\n\n")
        server.stop(0)
        os._exit(0)
