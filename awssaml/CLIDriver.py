"""Implement Federated API and CLI Access Using SAML 2.0 and AD FS

Usage:
  awssaml <command> [PROFILE]
  awssaml --help
  awssaml --version

Commands:
  console   Open Console in the web browser
  api       Configure CPI access

Arguments:
  PROFILE   optional profile name

Options:
  -h, --help
  --version
"""

import logging
from sys import platform, exit

from . import __version__ as VERSION
from awssaml.commands import *

from docopt import docopt

module_logger = logging.getLogger('awssaml')

if platform == "linux" or platform == "linux2":
    from systemd.journal import JournalHandler

    module_logger.addHandler(JournalHandler())

def main():
    driver = CLIDriver()
    return driver.main()


class CLIDriver(object):
    def __init__(self):
        self.logger = logging.getLogger(name='awssaml.CLIDriver')

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
            self.logger.error("Cannot find command: '%s'.", command_name)
            print("Command '%s' does not exist. Please use `samlapi --help` for more information." % command_name)
            exit(1)

        command = commands[command_name](command_args)

        try:
            command.run()
        except KeyboardInterrupt:
            self.logger.error("Interrupted by user")
            print("Interrupted by user")
            exit(1)
