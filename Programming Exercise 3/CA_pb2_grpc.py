# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import CA_pb2 as CA__pb2


class CertificateAuthorityStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterClient = channel.unary_unary(
                '/CertificateAuthority/RegisterClient',
                request_serializer=CA__pb2.ClientInfo.SerializeToString,
                response_deserializer=CA__pb2.RegistrationResponse.FromString,
                )
        self.IssueCertificate = channel.unary_unary(
                '/CertificateAuthority/IssueCertificate',
                request_serializer=CA__pb2.ClientID.SerializeToString,
                response_deserializer=CA__pb2.Certificate.FromString,
                )


class CertificateAuthorityServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IssueCertificate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CertificateAuthorityServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterClient': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterClient,
                    request_deserializer=CA__pb2.ClientInfo.FromString,
                    response_serializer=CA__pb2.RegistrationResponse.SerializeToString,
            ),
            'IssueCertificate': grpc.unary_unary_rpc_method_handler(
                    servicer.IssueCertificate,
                    request_deserializer=CA__pb2.ClientID.FromString,
                    response_serializer=CA__pb2.Certificate.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CertificateAuthority', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CertificateAuthority(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CertificateAuthority/RegisterClient',
            CA__pb2.ClientInfo.SerializeToString,
            CA__pb2.RegistrationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IssueCertificate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CertificateAuthority/IssueCertificate',
            CA__pb2.ClientID.SerializeToString,
            CA__pb2.Certificate.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
