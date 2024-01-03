#!/bin/bash



# Compile the proto file into Python code
python -m grpc_tools.protoc \
    -I./protos \
    --python_out=./std_web_crawler/communication/grpc \
    --grpc_python_out=./std_web_crawler/communication/grpc \
    --pyi_out=./std_web_crawler/communication/grpc \
    ./protos/crawler_coordination.proto

# Post-processing step to modify the import statement
sed -i 's/import crawler_coordination_pb2 as crawler__coordination__pb2/import std_web_crawler.communication.grpc.crawler_coordination_pb2 as crawler__coordination__pb2/g' std_web_crawler/communication/grpc/crawler_coordination_pb2_grpc.py