#!/bin/bash

# Computes the total uploaded files size for a given query result
# Usage example: ia-query-size.sh 'subject:some_subject'

echo "scale=2;`ia search -i $1 | xargs -L1 ia list -c name,size,source | grep original | grep -v -E '.sqlite|.xml' | cut -f 2 | paste -sd+ | bc` / 1073741824" | bc
