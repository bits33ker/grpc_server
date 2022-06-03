# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import speech_pb2 as speech__pb2


class SpeechStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Recognize = channel.unary_unary(
                '/Speech/Recognize',
                request_serializer=speech__pb2.RecognizeRequest.SerializeToString,
                response_deserializer=speech__pb2.RecognizeResponse.FromString,
                )
        self.EchoTest = channel.unary_unary(
                '/Speech/EchoTest',
                request_serializer=speech__pb2.RecognizeTest.SerializeToString,
                response_deserializer=speech__pb2.RecognizeTestEcho.FromString,
                )


class SpeechServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Recognize(self, request, context):
        """Performs synchronous speech recognition: receive results after all audio
        has been sent and processed.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EchoTest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SpeechServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Recognize': grpc.unary_unary_rpc_method_handler(
                    servicer.Recognize,
                    request_deserializer=speech__pb2.RecognizeRequest.FromString,
                    response_serializer=speech__pb2.RecognizeResponse.SerializeToString,
            ),
            'EchoTest': grpc.unary_unary_rpc_method_handler(
                    servicer.EchoTest,
                    request_deserializer=speech__pb2.RecognizeTest.FromString,
                    response_serializer=speech__pb2.RecognizeTestEcho.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Speech', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Speech(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Recognize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Speech/Recognize',
            speech__pb2.RecognizeRequest.SerializeToString,
            speech__pb2.RecognizeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EchoTest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Speech/EchoTest',
            speech__pb2.RecognizeTest.SerializeToString,
            speech__pb2.RecognizeTestEcho.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)