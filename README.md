Radar Web Monitor
=================


## Setup

```
poetry install
scripts/build_gRPC_server.sh
cd scripts/install_systemctl_user_unit.sh
cd ..

systemctl --user enable radar-web-monitor
systemctl --user start radar-web-monitor
```

## Connect

Browse [localhost:8000](localhost:8000)
