import click

from fml.client import output
from fml.client.cli.common import main, AliasedGroup
from fml.client.client import Client
from fml.common.ci.client import CIClient


@main.group('ci', cls = AliasedGroup)
def ci_service() -> None:
    """
    CI stuff
    """
    pass


@ci_service.command(name = 'watch')
@click.argument('number_from_top', type = int, required = True)
@click.option(
    '--superseed', '-s',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Unwatch all other runs.',
)
def watch(number_from_top: int, superseed: bool):
    """
    Watch CI run.
    """
    token = Client().latest_ci_token()
    client = CIClient(token['name'], token['value'])
    output.print_ci_checkers(
        Client().ci_watch(
            run_id = client.get_runs(start = number_from_top, limit = 1)[-1]['id'],
            superseed = superseed,
        )
    )


@ci_service.command(name = 'monitored')
def watching():
    """
    List currently watched CI runs.
    """
    output.print_ci_checkers(
        Client().ci_watching()
    )


@ci_service.command(name = 'list')
@click.option('--limit', '-l', default = 10, type = int, help = 'Limit.')
def runs_list(limit: int):
    """
    List latest CI runs
    """
    token = Client().latest_ci_token()
    client = CIClient(token['name'], token['value'])
    output.print_ci_runs(
        client.get_runs(limit = limit)
    )
