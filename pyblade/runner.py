import logging
import subprocess
import tempfile
from typing import Optional
from typing import Tuple

import numpy as np

from .config import RxConfig
from .config import TxConfig
from .sc16q11 import load_sc16q11

__all__ = [
    'run'
]

LOGGER = logging.getLogger(__name__)


def run(rx_config: RxConfig, scenario: Tuple[str, ...], tx_config: Optional[TxConfig] = None) -> np.ndarray:
    """
    Configure RX and optionally TX channels, run scenario and return received samples.

    Args:
        rx_config: Receiver (RX) configuration.
        tx_config: Transmitter (TX) configuration.
        scenario: BladeRF-CLI scenario (see examples and/or
         https://github.com/Nuand/bladeRF/blob/master/host/utilities/bladeRF-cli/README.md).

    Returns:
        np.ndarray of shape (n, x) where n is the number of the receiving channels
         and the x is the number of read samples.
    """
    with tempfile.NamedTemporaryFile() as rx_file, tempfile.NamedTemporaryFile() as tx_file:
        args = rx_config.as_args(rx_file.name)

        if tx_config is not None:
            args.extend(tx_config.as_args(tx_file.name))
            tx_config.write(tx_file.name)

        args.extend(scenario)

        bladerf_cli_full_scenario = '; '.join(args)
        LOGGER.debug('bladeRF-cl full scenario: %s', bladerf_cli_full_scenario)

        bladerf_cli_output = subprocess.check_output(['bladeRF-cli', '-e', bladerf_cli_full_scenario]).decode('utf-8')

        LOGGER.debug('bladeRF-cli console output: %s',
                     '\n'.join([i for i in bladerf_cli_output.splitlines() if i.strip()]))

        return load_sc16q11(rx_file.name, n_channels=len(rx_config.channels))
