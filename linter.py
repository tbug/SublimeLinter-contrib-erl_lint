from SublimeLinter.lint import Linter, util
from os.path import dirname, join

ERL_LINT = join(dirname(__file__), "erl_lint.erl")


class ErlLint(Linter):
    """Provides an interface to erlint."""

    syntax = 'erlang'
    cmd = ERL_LINT
    executable = None

    # hello.erl:7: error: {unbound_var,'J'}
    # hello.erl:5: warning: {unused_var,'X'}
    regex = (
        r'^.+?:(?P<line>\d+): '
        r'(?:(?P<error>error)|(?P<warning>warning)): '
        r'(?P<message>.+)'
    )
    multiline = False

    line_col_base = (1, 1)
    tempfile_suffix = '.erl'
    error_stream = util.STREAM_STDOUT
    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = None
