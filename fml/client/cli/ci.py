import datetime
import typing as t

import click

from fml.client import output
from fml.client.cli.common import main, AliasedGroup
from fml.client.client import Client
from fml.common.ci.client import CIClient


@main.group("ci", cls=AliasedGroup)
def ci_service() -> None:
    """
    CI stuff
    """
    pass


def _get_client() -> CIClient:
    token = Client().latest_ci_token()
    return CIClient(token["name"], token["value"])


@ci_service.command(name="watch")
@click.argument("number_from_top", type=int, required=False, default=0)
@click.option(
    "--timeout",
    "-t",
    type=str,
    required=False,
)
@click.option(
    "--superseed",
    "-s",
    default=False,
    type=bool,
    is_flag=True,
    show_default=True,
    help="Unwatch all other runs.",
)
def watch(number_from_top: int, timeout: t.Optional[str], superseed: bool):
    """
    Watch CI run.
    """
    if timeout is not None:
        from fml.client.dtmath.parse import DTMParser, DTMParseException

        try:
            timeout = DTMParser().parse(timeout)
        except (DTMParseException, ValueError) as e:
            print(e)
            return
        except TypeError:
            print("can't add dates")
            return
        if isinstance(timeout, datetime.timedelta):
            timeout += datetime.datetime.now()
        if timeout < datetime.datetime.now():
            print("timeout must be scheduled for future")
            return

    client = _get_client()
    output.print_ci_checkers(
        Client().ci_watch(
            run_id=client.get_runs(start=number_from_top, limit=1)[-1]["id"],
            timeout=timeout,
            superseed=superseed,
        )
    )


@ci_service.command(name="monitored")
def watching():
    """
    List currently watched CI runs.
    """
    output.print_ci_checkers(Client().ci_watching())


@ci_service.command(name="build-master")
def build_master():
    """
    Start new master build
    """
    client = _get_client()
    print(client.start_master_build().get("state"))


@ci_service.command(name="list")
@click.option("--limit", "-l", default=10, type=int, help="Limit.")
def runs_list(limit: int):
    """
    List latest CI runs
    """
    client = _get_client()
    output.print_ci_runs(client.get_runs(limit=limit))
