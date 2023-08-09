# skill-mark2-audio-receiver

## About

TODO: Write the skill around all these functions

This skill enables voice intents for the following audio receiver options on the Mycroft Mark 2 device:

- Airplay (via [UxPlay](https://github.com/FDH2/UxPlay))
- [KDE Connect](https://kdeconnect.kde.org/)
- Spotify (via [Raspotify](https://dtcooper.github.io/raspotify/))
- Bluetooth

It allows you to:

- Get the status of any of these services on the Mark 2
- Enable/disable the services
- Rename your devices in Airplay/Raspotify
- Pair Bluetooth/KDE Connect with other devices

Supported in Neon versions after mid-August (TODO: Specific version when it's available)

Requires [neon-phal-plugin-audio-receiver](), an admin PHAL plugin that handles the portions of the code that require `sudo`.

## Examples

- "Is bluetooth enabled?"
- "Is airplay enabled?"
- "Is Spotify enabled?"
- "Is KDE Connect enabled?"
- "Disable airplay"
- "Deactivate bluetooth"
- "Enable KDE Connect"
- "Activate Spotify"
- "Rename Airplay device"
- "Rename Spotify device"
- "Pair Bluetooth"
- "Pair KDE Connect"

## Credits

[Mike Gray](@mikejgray)

## Category

Device Control

## Tags

#Neon #devicecontrol #spotify #kdeconnect #airplay #bluetooth #mark2 #audio #cast

## Testing

`pytest -vvv --cov=skill_mark2_audio_receiver` will execute the unit tests, which can run in any environment.

For integration testing, clone this repo on a Mark 2 with the mid-August Neon image or later and execute `/home/neon/venv/bin/python tests/integration/integration.py`

The `integration.py` file has a couple of commented tests - these are the auto-pairing tests and tests to set device names. Since those require external interaction it's best to run them one at a time as you're ready.
