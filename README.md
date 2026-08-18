# simplesovd

A simple implementation of SOVD (Service Oriented Vehicle Diagnostics),
ISO 17978.

## Description

simplesovd is a tiny SOVD (Service Oriented Vehicle Diagnostics, ISO 17978)
implementation on top of Python FastAPI. It's intended solely for
research and/or POC purposes, not for production.

simplesovd currently suppports:
* Forward SOVD requests to backend entity servers
* Issuing UDS on CAN requests from UDSGateway function
  * This is a special case. In fact, an SOVD CDA is also an SOVD entity server.
    simplesovd transparently following the 'href' keyword in your
    configuration file.
* Some administrative command (outside SOVD entity namespace)
  * Access to '/admin' without vendor_prefix

simplesovd does not support:
* Other SOVD features than data, bulk-data.
* DoIP
* Multiple CAN interfaces
* AuthN/AuthZ
* TLS termination

## Usage

Preparation.
```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Run the application.
```
$ uvicorn main:app --port 7690
```

Append `--reload` if you like.

'simplesovd' uses a vendor prefix 'simplesovd/v1' currently.
Thus, access to 'http://localhost:7690/simplesovd/v1/areas' etc.
Also, you can define your own vehicle ECU topology using 'config.yaml'

simplesovd refers some environment variables.

* SIMPLESOVD_CONFIG
  * You can specify your config file.
* SIMPLESOVD_DEBUG
  * If you set any value other than 0, simplesovd runs in debug mode.

## TODO
* Re-write URLs contained in responses from backend entity servers
* Add more SOVD features support
* Enhance built-in CDA

## License
Apache License, Version 2.0

## Author
Masanori Itoh <masanori.itoh@gmail.com>

## References
### Standards
* ASAM SOVD
  * https://www.asam.net/standards/detail/sovd/
* ISO 17978-1 - Part 1: General information, definitions, rules and basic principles
  * https://www.iso.org/standard/85133.html
* ISO 17978-2 - Part 2: Use cases definition
  * https://www.iso.org/standard/86586.html
* ISO 17978-3 - Part 3: Application programming interface (API)
  * https://www.iso.org/standard/86587.html
* ISO Standards Maintenance Portal (ISO17978)
  * https://standards.iso.org/iso/17978/
### Open Source Software
* Eclipse OpenSOVD
  * https://projects.eclipse.org/proposals/eclipse-opensovd
  * https://github.com/eclipse-OpenSOVD
* sovd-lab by Mauro Cerrato
  * https://github.com/MauroCerrato/sovd-lab
### General readings
* Diagnostics Demystified by Mauro Cerrato
  * https://maurocerrato.github.io/diagnostics-demystified/
