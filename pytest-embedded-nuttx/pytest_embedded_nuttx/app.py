import logging
import re
from argparse import Namespace
from pathlib import Path

from esptool.cmds import FLASH_MODES, LoadFirmwareImage, image_info
from pytest_embedded.app import App


class NuttxApp(App):
    """
    NuttX App class for Espressif devices.
    Evaluates binary files (firmware and bootloader) and extract information
    required for flashing.

    Attributes:
        file_extension (str): app binary file extension.
    """

    def __init__(
        self,
        file_extension='.bin',
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.flash_size = None
        self.flash_freq = None
        self.flash_mode = None
        self.target = None
        self.file_extension = file_extension
        self.app_file, self.bootloader_file = self._get_bin_files()
        self._get_binary_target_info()

    def _get_bin_files(self) -> list:
        """
        Get path to binary files available in the app_path.
        If either the application image or bootloader is not found,
        None is returned.

        Returns:
            list: path to application binary file and bootloader file.
        """
        search_path = Path(self.app_path)
        search_pattern = '*' + self.file_extension
        bin_files = list(search_path.rglob(search_pattern))
        app_file, bootloader_file = None, None

        if not bin_files:
            logging.warning('No binary files found with pattern: %s', search_pattern)

        for file in bin_files:
            if 'nuttx' in str(file):
                app_file = file
            if 'mcuboot-' in str(file):
                bootloader_file = file

        return app_file, bootloader_file

    def _get_binary_target_info(self):
        """Binary target should be in the format nuttx.merged.bin, where
        the 'merged.bin' extension can be modified by the file_extension
        argument.

        Important note regarding MCUBoot:
        If enabled, the magic number will be on the MCUBoot binary. In this
        case, image_info should run on the mcuboot binary, not the NuttX one.
        """

        def get_key_from_value(dictionary, val):
            """Get key from value in dictionary"""
            for key, value in dictionary.items():
                if value == val:
                    return key
            return None

        binary_path = self.app_file
        if self.bootloader_file:
            binary_path = self.bootloader_file

        # Call esptool's image_info with the required args,
        # so the correct chip is identified in args.chip
        if binary_path:
            args = Namespace(filename=binary_path.as_posix(), chip='auto', version='2')
        else:
            return
        image_info(args)

        # Load app image and retrieve flash information
        image = LoadFirmwareImage(args.chip, binary_path.as_posix())
        self.target = re.sub(r'[-()]', '', args.chip.lower())

        # Flash Size
        flash_s_bits = image.flash_size_freq & 0xF0
        self.flash_size = get_key_from_value(image.ROM_LOADER.FLASH_SIZES, flash_s_bits)

        # Flash Frequency
        flash_fr_bits = image.flash_size_freq & 0x0F  # low four bits
        self.flash_freq = get_key_from_value(image.ROM_LOADER.FLASH_FREQUENCY, flash_fr_bits)

        # Flash Mode
        self.flash_mode = get_key_from_value(FLASH_MODES, image.flash_mode)
