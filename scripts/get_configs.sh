#!/bin/bash

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate fuzz4all

# Generate config and script
get_config() {
    MODEL_NAME="starcoder"
    MODEL_PARAMS="3b"
    OUTPUT_PARENT="outputs/${MODEL_NAME}_${MODEL_PARAMS}"
    if [ ! -d $OUTPUT_PARENT ]; then
        mkdir -p $OUTPUT_PARENT
    fi

    python tools/generate_config.py \
        --base-config "config/$1_demo.yaml" \
        --output-folder "$OUTPUT_PARENT/$1_$2" \
        --model "ollama/$MODEL_NAME:$MODEL_PARAMS" \
        --target "targets/gcc-13/bin/$3" \
        --iterations 6000 \
        --batch-size 30 \
        --time 24
}

# Do two runs for C and C++
for i in {1..2}; do
    get_config c $i gcc
    get_config cpp $i g++
done

# Deactivate conda environment
conda deactivate
