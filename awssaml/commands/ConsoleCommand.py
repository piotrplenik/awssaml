"""Console command"""

from .Base import Base
from awssaml.api.Authentication import Authentication
import webbrowser
import sys

class ConsoleCommand(Base):
    """Say hello, world!"""

    def run(self):
        authentication = Authentication(self.get_profile())
        sts = authentication.authenticate()

        request_url = sts.get_console_url()

        if not webbrowser.open_new_tab(request_url):
            raise Exception('Unable to open a browser to visit: {}'.format(request_url))

        # Give the user some basic info as to what has just happened
        print('You should have opened AWS Console in the new browser tab.')

        sys.exit(0)
