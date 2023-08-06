#!/bin/bash

# Duration in seconds to accept all pair requests
DURATION=30

# End time
END_TIME=$(($(date +%s) + DURATION))

# Loop until the duration has passed
while [ $(date +%s) -lt $END_TIME ]; do
  # List all available devices, filter unpaired ones, and accept the pairing requests
  kdeconnect-cli -l | grep -B 1 "is not paired" | grep "device id" | cut -d ":" -f 2 | xargs -I {} kdeconnect-cli --pair --id={}
  
  # Wait for a short period before checking again
  sleep 5
done
