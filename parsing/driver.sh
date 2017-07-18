#!/bin/bash

for N in $(seq 1 10); do
    ## feed word list to the python mapper here and redirect STDOUT to a temporary file on disk
    ####
    ####
    ./mapper.py  $N 'food_common' 'ACEI'  > res.$N.txt  &
    ####
    ####
done
## wait for the mappers to finish their work
wait