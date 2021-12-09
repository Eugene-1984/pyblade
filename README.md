# pyblade

Python BladeRF wrapper with tests and experiments. Wrapper aim to eliminate a boilerplate code to configure channels
and save/store signals as numpy arrays.

## Prerequisites for GNU/Linux OS:

Install the package and check that the `bladeRF-cli` utility exists in `PATH`,
the output with no device connected is:

```bash
$ sudo pacman -S bladerf

$ bladeRF-cli -p

  probe: No devices are available. If one is attached, ensure it
         is not in use by another program and that the current
         user has permission to access it.
``` 

After the actual blade is connected you can probe it (no root privilage is needed to access the CLI):
```bash
$ bladeRF-cli -p

  Description:    Nuand bladeRF 2.0
  Backend:        libusb
  Serial:         XXXXXXXXXXXXXXXXXXXXXXXXXX
  USB Bus:        2
  USB Address:    3
```

## Installation in developer mode

The python version in the OS disto may differ from the required version, we use https://github.com/pyenv/pyenv
tool to install a specific version. Install the prerequisites for your OS as described in
https://github.com/pyenv/pyenv/wiki#suggested-build-environment and then install python, activate venv and install 
`pyblade/requirements.txt`:

```bash
$ pyenv local 3.8.6
$ python -m venv venv
$ . ./venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install -r pyblade/requirements.txt
```

Typicall dev usage of the package is to install it in editable mode:
```bash
$ pip install -e pyblade
```

## Usages and example

Wrapper works in the "scenario" mode: the user creates receiver and/or transmitter configs and writes BladeRF-CLI
script:

```python
import pyblade

rx_config = pyblade.RxConfig(
    samplerate='4M',   # sample rate
    frequency=433e6,   # central frequency 
    bandwidth='2M',    # bandwidth
    n_samples='1M',    # number of samples to read
    agc=None,          # disable AGC
    channels=(1, 2),   # read from channel 1 and 2
)

iq = pyblade.run(
    rx_config=rx_config,
    scenario=('rx start',
              'rx',
              'rx wait')
)

# `iq` variable now hols a numpy array with the received samples.
```

Most of the examples are in the jupyter notebooks in the
[pyblade_examples](https://github.com/Eugene-1984/pyblade/tree/main/pyblade_examples directory). 