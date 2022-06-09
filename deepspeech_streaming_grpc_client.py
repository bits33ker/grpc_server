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
from typing import Iterable, List

import av
import numpy as np
import audioop

def read_wav(wavfile):
    audio = av.open(wavfile)
    if len(audio.streams.audio) > 1:
        logging.warning("Audio has more than one stream. Only one of them will be used.")

    resampler = av.audio.resampler.AudioResampler(
        format="s16", layout="mono", rate=16000
    )
    resampled_frames = []
    for frame in audio.decode(audio=0):
        resample = resampler.resample(frame)
        #for r in resample: 
        resampled_frames.append(resample.to_ndarray().flatten())

    #data8 = np.concatenate(resampled_frames, dtype=np.int16)
    return resampled_frames

def generate_stream(samples:List[bytes]) -> Iterable[speech_pb2.StreamingRecognizeRequest]:
    for s in samples:
        yield speech_pb2.StreamingRecognizeRequest(data = s)

async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = speech_pb2_grpc.SpeechStub(channel)
        data = read_wav('samples/testwav2.wav')
        l = []
        for i in data:
            #print(i[0:10])
            bi = audioop.lin2ulaw(i, 2)
            l.append(bi)
        speech_iterator = generate_stream(l)
        speech_summary = await stub.StreamingRecognize(speech_iterator)
        #speech_summary_future = stub.StreamingRecognize.future(speech_iterator)
        print("Speech client received: " + speech_summary.text)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())