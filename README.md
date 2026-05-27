# clinguin

## Installation

To install the project, run

```bash
pip install .
```

## Quick start

Terminal 1 — start the server:

```bash
clinguin server --domain-files tests/data/encoding.lp --ui-files tests/data/ui.lp --port 8000
```

Terminal 2 — start the client:

```bash
clinguin client --build
```

Open `http://127.0.0.1:8001` in your browser.

## Usage

Run the following for basic usage information:

```bash
clinguin -h
```

## Running tests

```bash
nox -s test
```

## Documentation

To generate and open the documentation, run

```bash
nox -s doc -- serve
```

Instructions to install and use `nox` can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md)
