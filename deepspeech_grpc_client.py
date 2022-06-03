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
"""The Python AsyncIO implementation of the GRPC speech.Greeter client."""

import asyncio
import logging

import grpc
import speech_pb2
import speech_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = speech_pb2_grpc.SpeechStub(channel)
        response = await stub.Recognize(speech_pb2.RecognizeRequest(data='samples/testwav2.wav'))
    print("Speech client received: " + response.text)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())