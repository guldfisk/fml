import os
import typing as t

import click

from fml.client.cli.context import OutputMode, Context
from fml.client.client import Client


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [
            x
            for x in
            self.list_commands(ctx)
            if x.startswith(cmd_name)
        ]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: {}'.format(', '.join(sorted(matches))))


force_option = click.option(
    '--force',
    '-f',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Never ask for confirmation.'
)


def split_text_option(text: str = 'target'):
    return click.argument(text, type = str, required = True, nargs = -1)


@click.group(cls = AliasedGroup)
@click.option('--output-mode', type = str, help = 'Formatting target for output.', default = 'table')
def main(output_mode: str) -> None:
    """
    Keep track of stuff and such.
    """
    if output_mode != 'table':
        options = [
            mode
            for mode in
            OutputMode
            if output_mode in mode.value
        ]
        if not len(options) == 1:
            print('invalid output mode {}'.format(output_mode))
        else:
            Context.output_mode = options[0]


@main.command(name = 'ding')
@click.option(
    '--blocking',
    '-b',
    default = False,
    type = bool,
    is_flag = True,
    show_default = True,
    help = 'Block while playing sound.'
)
def ding(blocking: bool) -> None:
    """
    Play alarm sound.
    """
    if blocking:
        from fml import sound
        sound.ding()
    else:
        Client().ding()


def get_default_project(project: t.Optional[str] = None) -> t.Optional[str]:
    p = project or os.environ.get('DEFP')
    return p if p else None
