#!/usr/bin/env python
import os


class cd(object):
    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.directory)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.cwd)
