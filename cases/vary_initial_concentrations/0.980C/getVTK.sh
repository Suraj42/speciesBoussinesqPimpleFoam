#!/bin/bash

# Define the start and end values
start=0.0
end=24.0
increment=0.4

# Loop through the time values and execute foamToVTK
for time in $(seq $start $increment $end); do
    echo "Processing time $time"
    foamToVTK -time $time
done
