Radar Web Monitor
=================

## Prerequisites

* libpcap
* librealsense (by mmwave-capture-std)
* protobuf (libprotoc-dev, protobuf-compiler)

## Setup

```
poetry install
./scripts/build_gRPC_server.sh
cd scripts
./install_systemctl_user_unit.sh
cd ..

systemctl --user enable radar-web-monitor
systemctl --user start radar-web-monitor
```

### Realsense on nVidia Jetson

See: https://github.com/IntelRealSense/librealsense/issues/10416#issuecomment-1314342663

## Connect

Browse [localhost:8000](localhost:8000)
