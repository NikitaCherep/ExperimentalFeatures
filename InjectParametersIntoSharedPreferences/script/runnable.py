#!/usr/bin/env python3

# TODO:
#  1. Добавить функционал по конвертировании приложения в debuggable
#  2. Перезапустить апу

import os
import argparse
from pathlib import Path
from subprocess import check_output
from subprocess import run
import xml.etree.ElementTree as ElementTree

ENCODING: str = "UTF-8"  # or sys.stdout.encoding
HOME: str = str(Path.home())
ADB: str = HOME + "/Library/Android/sdk/platform-tools/adb"
CURRENT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
SHARED_PREF_PATH: str = "shared_prefs/BidMachinePref.xml"
SHARED_PREF_KEY_TEST_MODE: str = "bid_machine_test_mode"
SHARED_PREF_KEY_LOGGING_ENABLED: str = "bid_machine_logging_enabled"


class SharedPrefXMLParser:

    def __init__(self, xml_string: str) -> None:
        super().__init__()
        root_tag = "map"
        try:
            self.root_element = ElementTree.fromstring(xml_string)
            if self.root_element.tag != root_tag:
                self.root_element = ElementTree.Element(root_tag)
        except Exception:
            self.root_element = ElementTree.Element(root_tag)

    def remove_prev_tag(self, element: ElementTree.Element) -> None:
        tag_name = element.get("name")
        if tag_name is None:
            return

        remove_element_list = []
        for find_element in self.root_element.findall(".//*[@name='" + tag_name + "']"):
            remove_element_list.append(find_element)

        for remove_element in remove_element_list:
            self.root_element.remove(remove_element)

    def include_param(self, name: str, value) -> None:
        print("    Include param: " + name + " - " + value.__str__())
        if isinstance(value, bool):
            self.include_bool(name, value)
        else:
            self.include_string(name, value)

    def include_string(self, name: str, value: str) -> None:
        element = ElementTree.Element("string", {
            "name": name
        })
        element.text = value
        self.include_tag(element)

    def include_bool(self, name: str, value: bool) -> None:
        element = ElementTree.Element("boolean", {
            "name": name,
            "value": value.__str__().lower()
        })
        self.include_tag(element)

    def include_tag(self, element: ElementTree.Element) -> None:
        self.remove_prev_tag(element)
        self.root_element.append(element)

    def to_string(self) -> str:
        return ElementTree.tostring(self.root_element, ENCODING, "xml").decode(ENCODING)


parser = argparse.ArgumentParser(description="Enable Test Mode in release app through BidMachine SharedPreferences")
parser.add_argument("package_name",
                    metavar="package_name",
                    type=str,
                    nargs="?",
                    help="application package name, for example 'io.bidmachine.test.app'")
args = parser.parse_args()

package_name: str = args.package_name
shared_pref_full_path: str = "/data/data/" + package_name + "/" + SHARED_PREF_PATH

print("\nReceiving shared preference...")
try:
    shared_pref: str = check_output(["sh", "-c",
                                     "{} shell "
                                     "run-as {} "
                                     "cat {}".format(
                                         ADB, package_name, SHARED_PREF_PATH
                                     )]).decode(ENCODING)
except Exception:
    print("    FAIL - Shared preference is missing.")
    shared_pref = ""

print("\nInject debug tags...")
shared_pref_xml_parser = SharedPrefXMLParser(shared_pref)
shared_pref_xml_parser.include_param(SHARED_PREF_KEY_TEST_MODE, True)
shared_pref_xml_parser.include_param(SHARED_PREF_KEY_LOGGING_ENABLED, True)

print("\nWrite shared preference...")
run(["sh", "-c",
     "{}/write_content_to_file.sh {} '{}'".format(
         CURRENT_DIR_PATH, shared_pref_full_path, shared_pref_xml_parser.to_string()
     )])

print("\nWork completed successful\n")
