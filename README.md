# Enterprise AI Copilot

An enterprise knowledge and workflow assistant combining business
analytics, document retrieval, and approval-based automation.

## Current status

Sprint 01 — Project initialization.

The local Git repository and Python virtual environment are initialized.
Application features are not implemented yet.

## Planned capabilities

- Analyze order and delivery data using SQL.
- Retrieve policy information with verifiable citations.
- Combine structured data and documents into business reports.
- Prepare workflow actions for human approval.

## Data sources

The first development phase will use the Olist Brazilian E-Commerce
Dataset. Dataset files are not included in this repository.

Demo company policies will be explicitly labeled as synthetic.
They must not be presented as official Olist policies.

## Development environment

- Python 3.14
- Git
- Python virtual environment: `.venv`

## Local setup

Run these commands from the repository root.

Create and activate a virtual environment on macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Verification

Check dependency consistency and run the smoke tests:

```bash
python -m pip check
python -m pytest
```

The current tests verify package imports and installed distribution metadata.
Business analytics features are not implemented yet.

## Reproduce the tested dependency versions

With Python 3.14 and an activated virtual environment, run:

```bash
python -m pip install -r requirements-dev.txt
python -m pip install -e ".[dev]"
python -m pip check
python -m pytest
```

`requirements-dev.txt` records the tested third-party dependency versions.
It is an environment snapshot, not a cross-platform lockfile.
