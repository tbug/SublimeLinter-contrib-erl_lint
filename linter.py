from SublimeLinter.lint import Linter, util
import os
from os import path

class ErlLint(Linter):
    """Provides an interface to erlc."""

    syntax = (
        "erlang"
    )

    executable = "erlc"
    tempfile_suffix = "erl"
    unique_file_in_root = "Makefile"
    lib_folder = path.join("_build","default","lib")

    # ERROR FORMAT # <file>:<line>: [Warning:|] <message> #
    regex = (
        r".+:(?P<line>\d+):"
        r"(?:(?P<warning>\sWarning:\s)|(?P<error>\s))"
        r"+(?P<message>.+)"
    )

    error_stream = util.STREAM_STDOUT

    defaults = {
    }

    def cmd(self):
        """
        return the command line to execute.
        this func is overridden so we can handle included directories.
        """
        command = [self.executable_path, '-Wall', '+strong_validation']

        ch_dir = self.get_chdir(self.get_view_settings())
        root_dir = self.find_build_folder_dir(path.dirname(ch_dir))
        if root_dir is None:
            return command
        lib_folder = path.join(root_dir, self.lib_folder)

        ebin_dirs = []
        for lib in os.listdir(lib_folder):
            p = path.join(lib_folder, lib, 'ebin')
            if path.isdir(p):
                ebin_dirs.append(p)

        for ebin_dir in ebin_dirs:
            command.extend(["-pa", ebin_dir])
        return command

    def find_build_folder_dir(self, directory, tries=5):
        if self.unique_file_in_root in os.listdir(directory):
            return directory
        elif tries > 0:
            return self.find_build_folder_dir(path.dirname(directory), tries - 1)
        else:
            return None

