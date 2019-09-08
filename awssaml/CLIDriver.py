"""usage:
  awssaml <command> [PROFILE]
  awssaml --version

Commands:
  console   Open Console in the web browser
  api       Open Console in the web browser

Arguments:
  PROFILE   optional profile name

Options:
  -h, --help
  --version
"""

import sys

from . import __version__ as VERSION
from awssaml.commands import *

from docopt import docopt


def main():
    driver = CLIDriver()
    return driver.main()


class CLIDriver(object):
    def main(self):
        """Main CLI entrypoint."""
        args = docopt(__doc__,
                      version="samlapi version " + VERSION,
                      options_first=True)

        command_name = args['<command>']
        command_args = {'profile': args['PROFILE']}

        commands = {
            "console": ConsoleCommand,
            "api": ApiCommand,
        }

        if not command_name in commands:
            print("Command '%s' does not exist. Please use `samlapi --help` for more information." % command_name)
            sys.exit(1)

        command = commands[command_name](command_args)
        command.run()
