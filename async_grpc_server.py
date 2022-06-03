# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python AsyncIO implementation of the GRPC speech.Greeter server."""

import asyncio
import logging

import grpc
import speech_pb2
import speech_pb2_grpc


class DeepSpeech(speech_pb2_grpc.SpeechServicer):

    async def Recognize(
            self, request: speech_pb2.RecognizeRequest,
            context: grpc.aio.ServicerContext) -> speech_pb2.RecognizeResponse:
        return speech_pb2.RecognizeResponse(message='Hello, %s!' % request.name)

    async def EchoTest(
            self, request: speech_pb2.RecognizeTest,
                        context: grpc.aio.ServicerContext) -> speech_pb2.RecognizeTestEcho:
        return speech_pb2.RecognizeTestEcho(echo=request.msg)

async def serve() -> None:
    server = grpc.aio.server()
    speech_pb2_grpc.add_SpeechServicer_to_server(DeepSpeech(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) 
    asyncio.run(serve())
