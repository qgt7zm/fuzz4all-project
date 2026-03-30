#/bin/sh

BATCH_SIZE="30"
MODEL_NAME="ollama/starcoder"
TARGET="targets/cvc5/bin/cvc5" # Can also use Z3

python Fuzz4All/fuzz.py --config config/smt_demo.yaml main_with_config \
    --folder outputs/smt_demo/ \
    --batch_size $BATCH_SIZE \
    --model_name $MODEL_NAME \
    --target $TARGET
