#!/usr/bin/env python
"""
update-certifi.py
~~~~~~~~~~~~~~~~~

This script updates all the certifi repositories to use a newer version of the
certifi certificate file. Run it after receiving an email alerting you to a
new certifi .pem file.

The script performs the following tasks:

- Takes a clean checkout of each of the certifi repositories.
- Changes into the directory.
- Runs `invoke update`.

The expectation is that `invoke update` will take care of downloading the new
copies of the .pem file, committing the changes, pushing them to GitHub and
doing anything needed to update the release. These actions vary per repository
and language, so are not specified in this file.
"""
import envoy
import os
import tempfile
import shutil


repositories = ['python-certifi', 'gocertifi']


class TemporaryDirectory(object):
    """
    A context manager that creates a temporary directory and switches to it.
    Ensures that the directory is cleaned up on completion.
    """
    def __init__(self):
        self.old_directory = None
        self.new_directory = None

    def __enter__(self):
        # Create a temp directory and switch to it.
        self.old_directory = os.getcwd()
        self.new_directory = tempfile.mkdtemp()
        os.chdir(self.new_directory)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        # Change back to the old directory.
        os.chdir(self.old_directory)

        # Clean up the directory.
        shutil.rmtree(self.new_directory)

        # Don't suppress exceptions
        return False


def exec_or_fail(command):
    rc = envoy.run(command)
    if rc.status_code:
        print "Failed to run %s" % command
        print "Stdout:"
        print r.std_out
        print "Stderr:"
        print r.std_err
        raise ValueError(rc.status_code)


def main():
    with TemporaryDirectory() as temp:
        # Update each repository in turn.
        for repo in repositories:
            # Clone it.
            exec_or_fail('git clone https://github.com/certifi/' + repo)

            # Switch into it.
            os.chdir(repo)

            # Run the invoke script.
            exec_or_fail('invoke update')

            # Switch back.
            os.chdir(temp.new_directory)


if __name__ == '__main__':
    main()
