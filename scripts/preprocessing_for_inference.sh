#!/bin/sh

CASE_ID=$(printf "%05d" $1)
BASE_DIR=$2
CASE_NAME=mini_pc_new_cascaded_dataset
CAP_DIR=./data/$CASE_NAME/capture_$CASE_ID
DATA_DIR=./data/$CASE_NAME/data-$CASE_NAME-capture_$CASE_ID-cascaded
OUTPUT_DIR=output/mini_pc_new_script_out_$CASE_NAME_$CASE_ID/

poetry run python scripts/proc_scripts/preprocessing_radar.py \
       $CAP_DIR \
       $DATA_DIR \
       --record_index=0 \
       -o $OUTPUT_DIR;
