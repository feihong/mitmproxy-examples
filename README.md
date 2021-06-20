# Feihong's mitmproxy examples

`mitmproxy` is an HTTPS proxy, here we collect a few examples of its usage.

## Prerequisites

    brew install python
    pip3 install pipenv

## Install

    pipenv shell
    pipenv install

Upgrade

    pipenv update

## Commands

Upgrade mitmproxy

    pipenv update mitmproxy

Start web interface (will open window in default browser automatically)

    mitmweb

Start proxy, dump downloaded files in `dumpfile`, don't cache:

    mitmdump -w dumpfile --anticache

Run `script.py` on contents of `dumpfile`:

    mitmdump -ns script.py -r dumpfile

## Links
