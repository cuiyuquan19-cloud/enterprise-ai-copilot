# Olist Data Exploration — Sprint 01, Day 2

## Scope and reproduction

Explored the nine CSV files acquired on 2026-10-25.
See [data_source.md](data_source.md) for provenance and licensing.

From the project root, with the virtual environment activated:

```bash
python -m enterprise_ai_copilot.explore_olist \
  --data-dir data/raw/olist/extracted
```

Raw files remain unchanged and excluded from Git.

## Parsing rules

- Load identifiers and other source fields as pandas strings.
- Interpret empty fields as missing; preserve literal NA/NULL text.
- Whitespace-only strings are not classified as missing.
- Convert selected numeric and timestamp fields for inspection.
- Parse timestamps without assigning an unverified timezone.
- Count duplicate occurrences after the first occurrence.

## Inventory and observed grain

| File | Rows | Columns | Observed grain / key findings |
|---|---:|---:|---|
| Customers | 99,441 | 5 | customer_id unique; customer_unique_id repeats |
| Geolocation | 1,000,163 | 5 | Multiple records per ZIP-code prefix |
| Order items | 112,650 | 7 | Unique (order_id, order_item_id) |
| Payments | 103,886 | 5 | Unique (order_id, payment_sequential) |
| Reviews | 99,224 | 7 | Unique (review_id, order_id); neither alone unique |
| Orders | 99,441 | 8 | order_id and customer_id individually unique |
| Products | 32,951 | 9 | product_id unique |
| Sellers | 3,095 | 4 | seller_id unique |
| Category translation | 71 | 2 | Both category-name columns individually unique |

Observed uniqueness is evidence for modeling, not a permanent
business constraint.

## Relationships and join risks

All checked nonmissing references matched their parent tables:
orders to customers; items to orders, products, and sellers;
payments and reviews to orders.

| Child table | Orders with no records | Orders with multiple records | Maximum records per order |
|---|---:|---:|---:|
| Items | 775 | 9,803 | 21 |
| Payments | 1 | 2,961 | 29 |
| Reviews | 768 | 547 | 3 |

Child-record totals reconcile with their source row counts.

Inner joins can exclude orders without child records.
Joining multiple child tables directly can multiply rows and inflate
counts or amounts. Product price, freight value, and payment value
must remain distinct measures until KPI definitions are agreed.

## Missing values and category coverage

- Customer delivery timestamps are missing for 2,965 orders.
- Approval timestamps are missing for 160 orders.
- Carrier delivery timestamps are missing for 1,783 orders.
- Review titles are missing for 87,656 records; messages for 58,247.
  Missing text does not imply a missing review score.
- Product categories are missing for 610 products.
- Another 13 products have categories absent from translation:
  - portateis_cozinha_e_preparadores_de_alimentos: 10 products
  - pc_gamer: 3 products
- All 71 translation entries occur in the products table.
- Product name length, description length, and photo quantity each
  have 610 missing values; overlap was not checked.
- Weight and each dimension field have two missing values.

## Orders and timestamps

Purchase timestamps range from 2016-09-04 to 2018-10-17.
All nonmissing values in the five checked order timestamp fields
parsed successfully.

| Status | Orders | Missing customer delivery timestamp |
|---|---:|---:|
| delivered | 96,478 | 8 |
| shipped | 1,107 | 1,107 |
| canceled | 625 | 619 |
| unavailable | 609 | 609 |
| invoiced | 314 | 314 |
| processing | 301 | 301 |
| created | 5 | 5 |
| approved | 2 | 2 |

Eight delivered orders lack delivery timestamps, while six canceled
orders have delivery timestamps. Causes remain unverified.

No parsed customer delivery or estimated delivery timestamp precedes
purchase. Other chronology relationships were not checked.

Missing delivery timestamps must not automatically mean on time
or late. Status eligibility, timezone assumptions, and calendar-date
versus exact-timestamp comparisons remain open for KPI design.

## Numeric observations

All checked nonmissing numeric fields converted successfully.

- 383 item records have zero freight value.
- Two payment records have zero installments.
- Nine payment records have zero payment value.
- Four products have zero weight.
- Review scores range from 1 to 5; integer-only values were not checked.
- Coordinate extremes need geographic investigation.
  Negative coordinates alone are not errors.

These observations do not justify automatic deletion or correction.

## Geolocation

- Fully duplicated rows after the first occurrence: 261,831.
- Distinct full rows: 738,332.
- Distinct ZIP-code prefixes: 19,015.
- Prefixes with multiple distinct full rows: 17,823.
- Prefixes with multiple distinct coordinate pairs: 17,781.
- Maximum distinct full rows per prefix: 779.
- Maximum distinct coordinate pairs per prefix: 746.

Coordinate distinctness was evaluated using source strings.
Removing identical rows does not make ZIP-code prefixes unique.
Direct joins on prefixes can multiply records.

## Limits and next steps

This is exploratory profiling, not automated data validation.
Formal schema, constraints, geolocation aggregation, monetary
representation, and KPI definitions remain for later days.

No database import, RAG, or Agent functionality is implemented.