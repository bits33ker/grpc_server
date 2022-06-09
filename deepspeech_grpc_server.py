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
import time
from typing import AsyncIterable, Iterable

import grpc
import speech_pb2
import speech_pb2_grpc
from deepspeech import Model
import deepspeech_server.decoding as decoding
import argparse
from scipy.io import wavfile
import numpy as np
import io
import av
import audioop

class GrpcSpeech(speech_pb2_grpc.SpeechServicer):
    def __init__(self, model_path, scorer, beam_width, lm_alpha, lm_beta):
        print("creating model {} with scorer {}...".format(model_path, scorer))
        self.model = Model(model_path)

        if scorer is not None:
            self.model.enableExternalScorer(scorer)
            if lm_alpha is not None and lm_beta is not None:
                if self.model.setScorerAlphaBeta(lm_alpha, lm_beta) != 0:
                    raise RuntimeError("Unable to set scorer parameters")

        if beam_width is not None:
            if self.model.setBeamWidth(beam_width) != 0:
                raise RuntimeError("Unable to set beam width")

        print("model is ready.")

    async def StreamingRecognize(self, request_iterator: AsyncIterable[
            speech_pb2.StreamingRecognizeRequest],
            context: grpc.aio.ServicerContext) -> speech_pb2.RecognizeResponse:       
        start_time = time.time()
        audio_count = 0
        resampled_frames = []
        async for audio in request_iterator:
            #print('StreamingRecognize ' + str(audio_count))
            audio_count += 1
            i16 = audioop.ulaw2lin(audio.data, 2)
            #l = len(audio.data);
            for d in range(0, int(len(i16)/2)):
                data = int.from_bytes(i16[d*2:d*2+2], byteorder='little', signed=True)
                resampled_frames.append(data)
            #print(i16[0:10])
            #resampled_frames.append(i16)
            
        elapsed_time = time.time() - start_time
        #data16 = np.concatenate(resampled_frames, dtype=np.int16)
        text = self.model.stt(resampled_frames)#data.astype(np.int16)
        #text = 'Hola Streaming Process'
        print("STT result: {}".format(text))
        return speech_pb2.RecognizeResponse(text=text)


    async def Recognize(
            self, request: speech_pb2.RecognizeRequest,
            context: grpc.aio.ServicerContext) -> speech_pb2.RecognizeResponse:
            if self.model is not None:
                try:
                    #samplerate, data = wavfile.read(request.data)
                    #w = wave.open(request.data, 'r')
                    #rate = w.getframerate()
                    #frames = w.getnframes()
                    #channels = w.getnchannels()
                    #buffer = w.readframes(frames)
                    #data = np.frombuffer(buffer, dtype=np.int16)
                    
                    audio = av.open(request.data)
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

                    data8 = np.concatenate(resampled_frames, dtype=np.int16)
                    # audio = decoding.decode_audio(io.BytesIO(data))
                    text = self.model.stt(data8)#data.astype(np.int16)
                    print("STT result: {}".format(text))
                except Exception as e:
                    print("STT error: {}".format(e), level=logging.ERROR)
            return speech_pb2.RecognizeResponse(text=text)

    async def EchoTest(
            self, request: speech_pb2.RecognizeTest,
                        context: grpc.aio.ServicerContext) -> speech_pb2.RecognizeTestEcho:
        return speech_pb2.RecognizeTestEcho(echo=request.msg)

async def serve() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', required=True, help='Modelo acustico')
    parser.add_argument('-s', '--scorer', required=False, help='Red KenLM')
    parser.add_argument('-bw', '--beam', required=False, help='Beam Width')
    parser.add_argument('-b', '--beta', required=False, help='Beta LM')
    parser.add_argument('-a', '--alpha', required=False, help='Alpha LM')
    ARGS = parser.parse_args()
    server = grpc.aio.server()
    speech_pb2_grpc.add_SpeechServicer_to_server(GrpcSpeech(model_path=ARGS.model, scorer=ARGS.scorer, beam_width=ARGS.beam, lm_beta=ARGS.beta, lm_alpha=ARGS.alpha), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) 
    asyncio.run(serve())
