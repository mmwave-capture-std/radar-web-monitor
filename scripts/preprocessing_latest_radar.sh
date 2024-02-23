#!/bin/sh

CASE_ID=$(printf "%05d" $1)
BASE_DIR=$2
CASE_NAME=cascaded_dataset
CAP_DIR=./data/$CASE_NAME/capture_$CASE_ID
DATA_DIR=./data/$CASE_NAME/$CASE_NAME-capture_$CASE_ID-cascaded
OUTPUT_DIR=output/script_out_$CASE_NAME_$CASE_ID/
DET_MODEL_PATH=../rtmpose-ort/rtmdet-nano
POSE_MODEL_PATH=../rtmpose-ort/rtmpose-m

run_with_time() {
    echo $@
    time "$@"
}

run_with_time poetry run python scripts/proc_scripts/preprocessing_radar.py \
       $CAP_DIR \
       $DATA_DIR \
       --record_index=0 \
       -o $OUTPUT_DIR;

run_with_time poetry run python scripts/proc_scripts/processing_radar_frames.py \
       $OUTPUT_DIR \
       $OUTPUT_DIR/doppler_fft/forward_triggered_frames-00000.pickle \
       --poses_input_file $OUTPUT_DIR/poses/poses_xyz.pickle \
       -o $OUTPUT_DIR \

run_with_time poetry run python scripts/proc_scripts/processing_superimpose.py \
       $OUTPUT_DIR \
       $OUTPUT_DIR/doppler_fft/forward_triggered_frames-00000.pickle \
       -o $OUTPUT_DIR \
