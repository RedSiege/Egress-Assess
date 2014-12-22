#!/usr/bin/env python

# This tool is designed to be an easy way to test exfiltrating data
# from the network you are currently plugged into.  Used for red or
# blue teams that want to test network boundary egress detection
# capabilities.


from common import helpers
from common import orchestra


if __name__ == "__main__":

    helpers.title_screen()

    cli_parsed = helpers.cli_parser()

    the_conductor = orchestra.Conductor()

    if cli_parsed.server is not None:
        the_conductor.load_server_protocols(cli_parsed)
        for full_path, server in the_conductor.server_protocols.iteritems():
            if server.protocol == cli_parsed.server.lower():
                server.serve()

    elif cli_parsed.client is not None:
        the_conductor.load_client_protocols(cli_parsed)
        the_conductor.load_datatypes(cli_parsed)
