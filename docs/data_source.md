# Olist Data Source

## Source and acquisition

- Dataset: Brazilian E-Commerce Public Dataset by Olist
- Provider: Olist, distributed through Kaggle
- Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Acquisition date: 2026-10-25
- Acquisition method: Manual download from Kaggle
- Dataset version: Not recorded
- License: CC BY-NC-SA 4.0
- License URL: https://creativecommons.org/licenses/by-nc-sa/4.0/

## Local files

- Downloaded archive: data/raw/olist/archive.zip
- Extracted files: data/raw/olist/extracted/
- CSV file count: 9
- Archive integrity check: Passed using python -m zipfile -t
- Archive SHA-256:
  967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784

The checksum identifies this downloaded archive. It has not been
compared with a publisher-provided checksum.

## Handling and publication

- Preserve the original archive and extracted CSV files unchanged.
- Exclude raw data from Git.
- Record exploration code and concise findings in the repository.
- Follow attribution, NonCommercial, and ShareAlike conditions when
  sharing licensed data or adaptations.
- Do not describe customer location or review data as risk-free.
- Label future simulated business policies as Synthetic Demo;
  they are not official Olist policies.

## Verification status

Archive integrity and the presence of nine CSV files are confirmed.
Row counts, columns, data types, missing values, duplicate records,
and key uniqueness have not yet been checked.
