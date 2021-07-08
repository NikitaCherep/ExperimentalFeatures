#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
from subprocess import run
from subprocess import check_output

ENCODING: str = "UTF-8"  # or sys.stdout.encoding
HOME: str = str(Path.home())
ADB: str = HOME + "/Library/Android/sdk/platform-tools/adb"
DEFAULT_EXTERNAL_DIR: str = "/sdcard"
CURRENT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
FEATURE_FILE_PATH: str = "files/features/DebugParameters.json"
PARAMETERS: str = open("parameters.json").read()

parser = argparse.ArgumentParser(description="Create debug file for test release app")
parser.add_argument("package_name",
                    metavar="package_name",
                    type=str,
                    nargs="?",
                    help="application package name, for example 'io.bidmachine.test.app'")
parser.add_argument("--clear",
                    action="store_true",
                    help="clear existent debug file")
args = parser.parse_args()

try:
    external_dir = check_output(["sh", "-c",
                                 "{} shell echo \\$EXTERNAL_STORAGE".format(ADB)]).decode(ENCODING).rstrip()
except Exception:
    external_dir = DEFAULT_EXTERNAL_DIR

package_name: str = args.package_name
feature_file_full_path: str = "{}/Android/data/{}/{}".format(external_dir, package_name, FEATURE_FILE_PATH)

if args.clear:
    print("\nRemoving file ...")
    run(["sh", "-c",
         "{} shell rm -f {}".format(
             ADB, feature_file_full_path
         )])
else:
    print("\nWrite parameters into file ...")
    run(["sh", "-c",
         "{}/write_content_to_file.sh {} '{}'".format(
             CURRENT_DIR_PATH, feature_file_full_path, PARAMETERS
         )])

print("\nWork completed successful\n")
