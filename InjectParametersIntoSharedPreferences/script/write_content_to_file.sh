#! /usr/local/bin/bash

readonly ADB_PATH="$HOME/Library/Android/sdk/platform-tools"
readonly TEMP_PATH="temp"

filePath=$1
content=$2

echo "    File path: $filePath"
echo "    Content: $content"

printf %s "$content" >"$TEMP_PATH"
"$ADB_PATH"/adb push "$TEMP_PATH" "$filePath"
rm "$TEMP_PATH"

exit
