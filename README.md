# simplesovd

A simple implementation of SOVD (Service Oriented Vehicle Diagnostics),
ISO 17973.

## Usage

Preparation.
```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements
```

Run the application.
```
$ uvicorn main:app --port 7690
```

Append `--reload` if you like.

'simplesovd' uses a vendor prefix 'simplesovd/v1' currently.
Thus, access to 'http://localhost:1920/simplesovd/v1/areas' etc.
Also, you can define your own vehicle topology using 'config.yaml'


## References
### Standards
* ASAM SOVD
  * https://www.asam.net/standards/detail/sovd/
* ISO 17988-1 - Part 1: General information, definitions, rules and basic principles
  * https://www.iso.org/standard/85133.html
* ISO 17988-2 - Part 2: Use cases definition
  * https://www.iso.org/standard/86586.html
* ISO 17988-3 - Part 3: Application programming interface (API)
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
