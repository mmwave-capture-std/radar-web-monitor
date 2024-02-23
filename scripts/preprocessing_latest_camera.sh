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

run_with_time poetry run python scripts/proc_scripts/preprocessing_camera.py \
       $CAP_DIR \
       --color --depth \
       -o $OUTPUT_DIR;

run_with_time poetry run python scripts/proc_scripts/preprocessing_camera_pose.py \
       $OUTPUT_DIR \
       $DET_MODEL_PATH \
       $POSE_MODEL_PATH \
       -o $OUTPUT_DIR;

rm latest
ln -s $OUTPUT_DIR/superimpose/ latest/
