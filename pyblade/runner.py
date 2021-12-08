import subprocess
import tempfile
from typing import Optional
from typing import Tuple
import os

import numpy as np

from .config import RxConfig
from .config import TxConfig
from .sc16q11 import load_sc16q11

__all__ = [
    'run'
]


def run(rx_config: RxConfig, scenario: Tuple[str, ...], tx_config: Optional[TxConfig] = None) -> np.ndarray:
    with tempfile.NamedTemporaryFile() as rx_file, tempfile.NamedTemporaryFile() as tx_file:
        args = rx_config.as_args(rx_file.name)

        if tx_config is not None:
            args.extend(tx_config.as_args(tx_file.name))
            tx_config.write(tx_file.name)

        args.extend(scenario)

        print('Executing bladeRF-cli with:\n', '\n'.join(args))

        bladerf_cli_output = subprocess.check_output(['bladeRF-cli', '-e', '; '.join(args)]).decode('utf-8')
        bladerf_cli_output = '\n'.join([i for i in bladerf_cli_output.splitlines()
                                        if i.strip()])  # remove empty lines

        print('bladeRF-cli output is:', bladerf_cli_output)

        return load_sc16q11(rx_file.name, n_channels=len(rx_config.channels))
