import math
from typing import BinaryIO
from typing import List

import numpy as np

__all__ = [
    'SC16Q11_DTYPE',
    'SC16Q11_FACTOR',
    'load_sc16q11',

]

SC16Q11_DTYPE = np.int16
SC16Q11_FACTOR = 2048


def _pack(signals_t: List[np.ndarray]) -> np.ndarray:
    packed = np.vstack([c for s_t in signals_t for c in (s_t.real, s_t.imag)]).transpose().flatten()
    return packed


def store_sc16q11(signals_t: List[np.ndarray], fid: BinaryIO, dtype=SC16Q11_DTYPE):
    (SC16Q11_FACTOR * _pack(signals_t)).astype(dtype).tofile(fid)


def load_sc16q11(file_name: str, n_channels: int = 1, iq_dtype=np.complex64) -> np.ndarray:
    """
    Load SC16Q11 binary file into numpy array

    Args:
        file_name: file name to a SC16Q11 binary file
        n_channels: number of channels
        iq_dtype: dtype for the output IQ samples

    Returns:
        numpy.ndarray of shape (n_channels, n_iq_samples_per_channel) where n_iq_samples_per_channel
        is the number of complex iq samples corresponding to each channel

    """
    with open(file_name, 'rb') as f:
        samples = np.fromfile(f, dtype=SC16Q11_DTYPE)
        n_iq_samples_per_channel = math.floor(len(samples) / n_channels / 2)
        iq = np.empty((n_channels, n_iq_samples_per_channel), dtype=iq_dtype)

        for channel in range(n_channels):
            iq[channel, :] = ((samples[2 * channel + 0::n_channels * 2] +
                               1j * samples[2 * channel + 1::n_channels * 2]) / SC16Q11_FACTOR)

    return iq
