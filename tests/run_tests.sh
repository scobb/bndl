#!/usr/bin/env bash

SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR/..

for test_case in $(ls tests | grep "^test"); do
    python tests/$test_case
done
