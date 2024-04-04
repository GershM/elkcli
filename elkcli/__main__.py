#!/usr/bin/env python3
import argparse
from shell.elkPrompt import ElkCliPrompt

import click

@click.command()
@click.option('-h', '--host',       type=str,   default="localhost",    help="host to connect to the Elastic Search [Default: localhost]")
@click.option('-p', '--port',       type=int,   default=9200,           help="Port number to use for connection [Default: 9200]")
@click.option('-k', '--insecure',               default=False,          help="Allow insecure server connections",                           is_flag=True )
@click.option('-u', '--username',   type=str,   default="elastic",      help="Username to connect to the Elastic Search [Default: elastic]")
@click.option('-vi',                                                    help='Host address of the database.',                               is_flag=True )
def main(host, port, insecure, username, vi):
    """A Elastic search terminal client with auto-completion and syntax highlighting.

    \b
    Examples:
      - elkcli
      - elkcli -h domain -vi -u username
    """

    args = argparse.Namespace(host=host, port=port, insecure=insecure, username=username, vi=vi)

    elkCliPrompt = ElkCliPrompt()
    elkCliPrompt.connect(args)
    elkCliPrompt.run()


if __name__ == "__main__":
    import sys
    sys.exit(main())
