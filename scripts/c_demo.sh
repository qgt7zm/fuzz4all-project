#/bin/sh

BATCH_SIZE="30"
MODEL_NAME="ollama/starcoder"

python Fuzz4All/fuzz.py --config config/c_demo.yaml main_with_config \
    --folder outputs/c_demo/ \
    --batch_size $BATCH_SIZE \
    --model_name $MODEL_NAME \
    --target targets/gcc-13/bin/gcc
