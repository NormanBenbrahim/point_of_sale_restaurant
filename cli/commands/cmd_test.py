import os
import subprocess

import click


@click.command()
@click.argument('path', default=os.path.join('app', 'tests'))
def cli(path):
    """
    tests with pytest

    path: test path
    return: call result
    """
    cmd = 'py.test {0}'.format(path)
    return subprocess.call(cmd, shell=True)
