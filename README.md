Based on Greeter Server
[This code's documentation lives on the grpc.io site.](https://grpc.io/docs/languages/python/quickstart)

https://grpc.io/docs/what-is-grpc/introduction/
https://grpc.io/docs/languages/python/basics/
https://github.com/googleapis/googleapis/blob/master/google/cloud/speech/v1/cloud_speech.proto
https://developers.google.com/protocol-buffers/docs/proto3

Proto:
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. speech.proto

