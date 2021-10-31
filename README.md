# Feihong's mitmproxy examples

`mitmproxy` is an HTTPS proxy, here we collect a few examples of its usage.

## Prerequisites

    pyenv install 3.10.0
    pyenv global 3.10.0

## Install

    make install

## Commands

Upgrade mitmproxy:

    make upgrade

Start web interface (will open window in default browser automatically)

    mitmweb

Start proxy, dump downloaded files in `dumpfile`, don't cache:

    mitmdump -w dumpfile --anticache

Run `script.py` on contents of `dumpfile`:

    mitmdump -ns script.py -r dumpfile

## Links

- [mitmproxy docs](https://docs.mitmproxy.org/stable/)
