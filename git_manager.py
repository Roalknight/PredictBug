#!/usr/bin/env python

from cd import cd
import os
import shutil
import subprocess
import tempfile
import stat

#TODO: Tải dataset về 

class Repository(object):

    def __init__(self, location):

        self.__tempdir = tempfile.mkdtemp()
        self.remote_location = location
        self.local_location = None

        self.__clone_remote()

    # enter and exit are called when the class is used in a "with" clause,
    # like:
    #
    # with Repository("git@github.com:Lab41/hermes.git") as hermes_repo:
    #     pass
    #
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean up the directory
        for root, dirs, files in os.walk(self.__tempdir, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        shutil.rmtree(self.__tempdir)

    def __clone_remote(self):
        with cd(self.__tempdir):
            command = [
                "git",
                "clone",
                "--",
                self.remote_location,
            ]
            subprocess.check_call(command)

        # Set the local directory. The only item in the directory will be the
        # repository.
        items = os.listdir(self.__tempdir)
        self.local_location = self.__tempdir + '/' + items[0]
