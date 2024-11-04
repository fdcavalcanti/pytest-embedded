from pytest_embedded_serial.dut import SerialDut

from .app import NuttxApp


class NuttxDut(SerialDut):
    """
    Dut class for serial ports connect to Espressif boards which are flashed with ESP-IDF apps

    Attributes:
        target (str): target chip type
        skip_check_coredump (bool): skip check core dumped or not while dut teardown if set to True
    """

    PROMPT_NSH = 'nsh>'
    PROMPT_TIMEOUT_S = 30

    def __init__(
        self,
        app: NuttxApp,
        **kwargs,
    ) -> None:
        self.target = app.target

        super().__init__(app=app, **kwargs)

    def reset_to_nsh(self, ready_prompt: str = PROMPT_NSH) -> None:
        """
        Resets the board and waits until the Nuttshell prompt appears.
        Defaults to 'nsh>'.
        """
        self.serial.hard_reset()
        self.expect(ready_prompt, timeout=self.PROMPT_TIMEOUT_S)

    def write(self, data: str) -> None:
        """Command to write on the Nuttshell prompt."""
        super().write(data)
