#!/bin/sh

cd submodules/cascaded-radar-capture-gRPC-server/ti/example/mmWaveLink_Cascade_Example/
cmake -Bbuild .
cmake --build build
cmake --install build
