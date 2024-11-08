### pytest-embedded-nuttx

Pytest embedded service for NuttX project alongside Espressif devices.

While using pytest-embedded standalone allows you to communicate with serial
devices and run simple tests, this module adds extra capabilities for Espressif devices,
such as flashing, rebooting and some improved parsing on the NuttShell.

Extra Functionalities:

- `app`: Explore the NuttX binary directory and identify firmware and bootloader files.
- `serial`: Parse the binary information and flash the board. Requires 'esp' service.
- `dut`:  Send commands to device through serial port. Requires 'esp' service.
