#!/usr/bin/env python3
#
# Since: January, 2019
# Author: gvenzl
# Name: unit_tests.py
# Description: Unit tests file for csv2db
#
# Copyright 2019 Gerald Venzl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import functions as f
import config as cfg
import unittest
import csv2db


class CSV2DBTestCase(unittest.TestCase):

    def setUp(self):
        # Set the default column separator for all tests
        cfg.column_separator = ","
        cfg.quote_char = '"'

    def test_open_csv_file(self):
        with f.open_file("../resources/201811-citibike-tripdata.csv") as file:
            self.assertIsNotNone(file.read())

    def test_open_zip_file(self):
        with f.open_file("../resources/201811-citibike-tripdata.csv.zip") as file:
            self.assertIsNotNone(file.read())

    def test_open_gzip_file(self):
        with f.open_file("../resources/201811-citibike-tripdata.csv.gz") as file:
            self.assertIsNotNone(file.read())

    def test_read_header(self):
        with f.open_file("../resources/201811-citibike-tripdata.csv.gz") as file:
            reader = f.get_csv_reader(file)
            expected = ["BIKEID", "BIRTH_YEAR", "END_STATION_ID", "END_STATION_LATITUDE",
                        "END_STATION_LONGITUDE", "END_STATION_NAME", "GENDER", "STARTTIME",
                        "START_STATION_ID", "START_STATION_LATITUDE", "START_STATION_LONGITUDE",
                        "START_STATION_NAME", "STOPTIME", "TRIPDURATION", "USERTYPE"]
            expected.sort()
            actual = f.read_header(reader)
            actual.sort()
            self.assertListEqual(expected, actual)

    def test_tab_separated_file(self):
        cfg.column_separator = "\t"
        with f.open_file("../resources/201812-citibike-tripdata.tsv") as file:
            reader = f.get_csv_reader(file)
            content = [f.read_header(reader)]
            for line in reader:
                content.append(line)
            self.assertEqual(11, len(content))

    def test_pipe_separated_file(self):
        cfg.column_separator = "|"
        with f.open_file("../resources/201812-citibike-tripdata.psv") as file:
            reader = f.get_csv_reader(file)
            content = [f.read_header(reader)]
            for line in reader:
                content.append(line)
            self.assertEqual(11, len(content))

    def test_exit_code_zero(self):
        self.assertEqual(0, csv2db.run(["gen", "-f", "../resources/201811-citibike-tripdata.csv.gz", "-t", "STAGING"]))

    def test_exit_code_two(self):
        # Test that command raises SystemExit exception
        with self.assertRaises(SystemExit) as cm:
            csv2db.run(["load", "-f", "../resources/201811-citibike-tripdata.csv.gz", "-t", "STAGING"])
        # Test that command threw SystemExit with status code 2
        self.assertEqual(cm.exception.code, 2)

    def test_exit_code_three(self):
        self.assertEqual(3,
                         csv2db.run(
                                    ["load",
                                     "-f", "../resources/201811-citibike-tripdata.csv",
                                     "-u", "test",
                                     "-p", "test",
                                     "-t", "STAGING"]
                                    )
                         )


if __name__ == '__main__':
    unittest.main()
