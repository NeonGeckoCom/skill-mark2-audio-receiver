#!/bin/bash

# Duration in seconds to accept all pair requests
DURATION=60

# Make PulseAudio accept all devices (replace this with specific rules as needed)
echo 'load-module module-native-protocol-tcp auth-ip-acl=0.0.0.0/0 auth-anonymous=1' | pacmd

# Set up bluetoothctl agent to auto accept pairing
echo -e 'agent on\ndefault-agent\npairable on' | bluetoothctl

# End time
END_TIME=$(($(date +%s) + DURATION))

# Loop until the duration has passed
while [ $(date +%s) -lt $END_TIME ]; do
  # Sleep for a short period before checking again
  sleep 5
done

# Turn off pairable mode
echo -e 'pairable off' | bluetoothctl

# Reset PulseAudio TCP module (if needed, based on your use case)
# Note that this will disconnect the newly paired user, so this is probably a bad idea
# echo 'unload-module module-native-protocol-tcp' | pacmd
