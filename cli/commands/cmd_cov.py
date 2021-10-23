import subprocess

import click


@click.command()
@click.argument('path', default='app')
def cli(path):
    """
    test coverage

    path: test coverage path
    return: call result
    """
    cmd = 'py.test --cov-report term-missing --cov {0}'.format(path)
    return subprocess.call(cmd, shell=True)
