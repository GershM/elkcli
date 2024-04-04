from rich.console import Console
from rich.spinner import Spinner
import time

class ElkSpinner:
    def __init__(self, spinner_type="point"):
        self.console = Console()
        self.spinner = Spinner(name = spinner_type, text = "Loading...")
        self.stop_spinner = False

    def start(self, functions, loading_status_text="Loading...", complete_status_text="", fail_status_text="Failed!"):
        try:
            with self.console.status("[bold green]{}\n".format(loading_status_text)) as status:
                while any(func() is False for func in functions):
                    time.sleep(0.5)
                    self.spinner.update()

            self.console.print("\r[bold green]{} [/]".format(complete_status_text))

        except Exception as e:
            self.console.print("\r[bold red]{} [/]".format(fail_status_text))
            self.console.print(e)
