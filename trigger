#!/usr/bin/env bash

n=$1
if [ -z "$n" ]; then
  n=1
fi

export $(cat dev.env | xargs)

echo


for i in $(seq 1 $n);
do
    curl \
        -H "Content-Type: application/json" \
        -d '{}' \
        -X POST ${TRIGGER_PROTOCOL}://localhost:${TRIGGER_EXT_PORT}/merchant_pos_new_checkout

    echo
    echo
done