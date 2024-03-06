#!/bin/sh

poetry run mmwavecapture-std configs/cascaded_realsense.toml
poetry run python scripts/get_latest_case_num.py
poetry run python concur.py
sh ./scripts/preprocessing_for_inference.sh `cat latest_case`
