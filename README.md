# pyblade

Python BladeRF wrapper with tests and experiments.

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

## Python deployment

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

