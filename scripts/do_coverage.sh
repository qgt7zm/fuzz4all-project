#!/bin/bash

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate fuzz4all

# Collect coverage for
get_coverage() {
    FOLDER="outputs/starcoder_3b/$1_$2"
    python tools/coverage/$3/collect_coverage.py \
        --folder $FOLDER \
        --interval $4
}

# Do two runs for C and C++
for i in {1..2}; do
    get_coverage c $i C 100
    get_coverage cpp $i CPP 100
done

# Deactivate conda environment
conda deactivate
