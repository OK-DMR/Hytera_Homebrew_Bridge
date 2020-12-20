#!/usr/bin/env python3

from typing import Type, Optional

from kaitaistruct import KaitaiStruct


def parse_test_data(
    class_name: Type[KaitaiStruct], glob_string: str, pretty_print: bool = True
) -> Optional[KaitaiStruct]:
    """
    :param class_name: type of struct to expect
    :param glob_string: glob for test files
    :param pretty_print: if set to false, will dump vars instead
    :return KaitaiStruct last tested file
    """
    from glob import glob

    testfile = None
    print("parseTestData: path: %s" % glob_string)
    for testfile in sorted(glob(glob_string)):
        print("----------")
        print("parseTestData: testfile: %s" % testfile)
        instance = class_name.from_file(testfile)
        if pretty_print:
            from hytera_homebrew_bridge.tests.prettyprint import prettyprint

            prettyprint(instance)
        else:
            print(vars(instance))

    return testfile
