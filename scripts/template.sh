#/bin/sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate fuzz4all

# Set variables
CONFIG_FILE="{CONFIG_FILE}"
OUTPUT_FOLDER="{OUTPUT_FOLDER}"
BATCH_SIZE="{BATCH_SIZE}"
MODEL_NAME="{MODEL_NAME}"
TARGET="{TARGET}"

# Run Fuzz4All
python Fuzz4All/fuzz.py --config $CONFIG_FILE main_with_config \
    --folder $OUTPUT_FOLDER \
    --batch_size $BATCH_SIZE \
    --model_name $MODEL_NAME \
    --target $TARGET

# Deactivate conda environment
conda deactivate
