# Feihong's mitmproxy examples

`mitmproxy` is an HTTPS proxy, here we collect a few examples of its usage.

## Prerequisites

### Linux

    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
    # Update ~/.profile and ~/.bashrc according to instructions, then logout and login

### Mac

    brew install pyenv

### Python

    pyenv install --list # list all versions you can install
    pyenv install 3.10.2
    pyenv global 3.10.2

## Installation

    make install

## Commands

Upgrade mitmproxy:

    make upgrade

Start web interface to view contents of dump file (will open window in default browser automatically)

    mitmweb -r dumpfile

Start proxy, dump downloaded files in `dumpfile`, don't cache:

    mitmdump -w dumpfile --anticache

Run `script.py` on contents of `dumpfile`:

    mitmdump -ns script.py -r dumpfile

## Links

- [mitmproxy docs](https://docs.mitmproxy.org/stable/)
