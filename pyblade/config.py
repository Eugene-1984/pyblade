from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, BinaryIO, Union

import numpy as np
from dataclasses import dataclass

from .helpers import human_to_float
from .sc16q11 import store_sc16q11

__all__ = [
    'RxConfig',
    'TxConfig'
]


@dataclass
class ConfigBase(ABC):
    samplerate: str
    frequency: Union[float, str]
    bandwidth: str
    channels: Tuple[int, ...]

    @property
    def samplerate_(self) -> float:
        return human_to_float(self.samplerate)

    @property
    def frequency_(self) -> float:
        return human_to_float(self.frequency)

    @property
    def bandwidth_(self) -> float:
        return human_to_float(self.bandwidth)

    @property
    @abstractmethod
    def _mode(self) -> str:
        ...

    @property
    def _config_channel(self) -> str:
        return ','.join(str(i) for i in self.channels)

    def as_partial_args(self) -> List[str]:
        args = []

        mode = self._mode

        for channel in self.channels:
            args.extend((f'set samplerate {mode}{channel} {self.samplerate}',
                         f'set frequency {mode}{channel} {self.frequency}',
                         f'set bandwidth {mode}{channel} {self.bandwidth}'))

        return args


@dataclass
class RxConfig(ConfigBase):
    n_samples: str
    agc: Optional[int]

    @property
    def n_samples_(self) -> int:
        return int(human_to_float(self.n_samples))

    @property
    def _mode(self) -> str:
        return "rx"

    def as_args(self, file_name: str) -> List[str]:
        args = self.as_partial_args()

        agc_enabled = self.agc is None

        args.append(f"set agc {'on' if agc_enabled else 'off'}")

        if not agc_enabled:
            for c in self.channels:
                args.append(f'set gain rx{c} {self.agc}')

        args.append(f"{self._mode} config file={file_name} "
                    f"channel={self._config_channel} "
                    f"n={self.n_samples}")

        return args


@dataclass
class TxConfig(ConfigBase):
    signals_t: List[np.ndarray]

    def __post_init__(self):
        if len(self.channels) != len(self.signals_t):
            raise ValueError

    @property
    def _mode(self) -> str:
        return "tx"

    def as_args(self, file_name: str) -> List[str]:
        args = self.as_partial_args()
        args.append(f"{self._mode} config file={file_name} "
                    f"channel={self._config_channel} "
                    f"format=bin "
                    f"repeat=0")
        return args

    def write(self, fid: BinaryIO):
        store_sc16q11(self.signals_t, fid)
