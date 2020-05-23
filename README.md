# Feihong's mitmproxy examples

`mitmproxy` is an HTTPS proxy, here we collect a few examples of its usage.

## Installation

```
brew install mitmproxy
```

Upgrade

    brew upgrade mitmproxy

## Commands

Start proxy, dump downloaded files in `dumpfile`, don't cache:

    mitmdump -w dumpfile --anticache

Run `script.py` on contents of `dumpfile`:

    mitmdump -ns script.py -r dumpfile

## Links
