import os
import typing as t

import click

from fml import sound


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
def main() -> None:
    """
    Keep track of stuff and such.
    """
    pass


@main.command(name = 'ding')
def ding() -> None:
    """
    Play alarm sound.
    """
    sound.play_sound()


def get_default_project(project: t.Optional[str] = None) -> t.Optional[str]:
    p = project or os.environ.get('DEFP')
    return p if p else None
