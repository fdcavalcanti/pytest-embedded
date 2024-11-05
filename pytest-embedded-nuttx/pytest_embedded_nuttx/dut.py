import logging
import re
from typing import AnyStr

import pexpect
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

    def return_code(self) -> int:
        """
        Matches the 'echo $?' response and extracts the integer value
        corresponding to the last program return code.

        Returns:
            int: return code.
        """
        self.write('echo $?')
        echo_match = self.expect(r'echo \$\?\r\n(\d+)', timeout=1)
        ret_code = re.findall(r'\d+', echo_match.group().decode())
        if not ret_code:
            logging.error('Failed to retrieve return code')
        return int(ret_code[0])

    def write_and_return(self, data: str, timeout: int = 2) -> AnyStr:
        """
        Writes to Nuttshell and returns all available serial data.

        Args:
            data: data to be passed on to Nuttshell.
            timeout: how long to wait for an answer in seconds.

        Returns:
            AnyStr
        """
        self.write(data)
        ans = self.expect(pexpect.TIMEOUT, timeout=timeout)
        return ans.rstrip().decode()
