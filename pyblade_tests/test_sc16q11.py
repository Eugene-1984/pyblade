import numpy as np
import tempfile

from pyblade.sc16q11 import store_sc16q11
from pyblade.sc16q11 import load_sc16q11


def test_single_channel_io():
    f_0 = 2
    t = np.arange(1024)
    s_t = np.exp(1j * 2 * np.pi * f_0 * t)
    with tempfile.NamedTemporaryFile() as f:
        store_sc16q11([s_t], f.name)
        y_t = load_sc16q11(f.name, n_channels=1)
        assert np.allclose(s_t, y_t)


def test_dual_channel_io():
    f_0 = 2
    t = np.arange(1024)
    s_t = np.exp(1j * 2 * np.pi * f_0 * t)
    with tempfile.NamedTemporaryFile() as f:
        store_sc16q11([s_t, -s_t], f.name)
        y_t, inv_y_t = load_sc16q11(f.name, n_channels=2)
        assert np.allclose(s_t, y_t)
        assert np.allclose(-s_t, inv_y_t)
