import typing as t

from rich.align import Align

from textual.app import App
from textual.widget import Widget

from fml.client import output
from fml.client.client import Client


class AlarmList(Widget):

    def __init__(self, name: t.Optional[str] = None) -> None:
        super().__init__(name)
        self._client = Client()

    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        return Align.center(
            output.print_alarms.get_table(
                Client().active_alarms()
            )
        )


class TestApp(App):
    async def on_mount(self):
        await self.view.dock(AlarmList())
