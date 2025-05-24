# Hydra Convert

**Hydra Convert** is a small command-line utility that turns plain-text “random-table” files into **Hydra Lists** library bundles (`.hllib`).  
Hydra Lists (Steam / itch.io) is a GUI dice-roller for Game Masters: import a bundle, click the dice icon, and it rolls results instantly.

---

## Project layout
```yaml
project/
├── hydra_convert.py                # converter script
├── inputs/                         # put your .txt source tables here
├── outputs/                        # finished .hllib bundles appear here
├── Book_of_Random_Tables_….xml     # example converted book
├── meta.hlmeta                     # example metadata
└── tests/                          # automated test-suite
    ├── test_make_book.py
    ├── test_list_type_mapping.py
    └── test_end_to_end.py
```

*(The `inputs/` and `outputs/` folders are created automatically if they don’t exist.)*

---

## Prerequisites

* Python ≥ 3.10  
* Install deps:

`pip install lxml pytest hypothesis`

* If you prefer a lockfile, add those to `requirements.txt` and run:

`pip install -r requirements.txt`.

---

## Usage

1. **Write a text file** inside `inputs/`, for example:
```YAML
My Dungeon Book
=Room Dressing
Broken weapon
Rusty key
Mossy statue
Dusty rug
```
*First line = book name. Each table starts with `=` followed by the table name.*

2. **Run the converter** from the project root:

        python hydra_convert.py

    For every `*.txt` in `inputs/` you’ll get `<Book_Name>.hllib` in `outputs/`.

3. **Import into Hydra Lists**

    Hydra Lists → Import → Library → choose the .hllib

    Click the dice icon to roll your freshly-minted tables.

---

## Running the tests

All automated tests live in `tests/`. They launch in a temporary workspace so your real data is never touched.

`pytest -q`



### What the tests cover

| Test file | Scope | Ensures |
|-----------|-------|---------|
| `test_make_book.py` | Unit tests for `make_book()` | XML is well-formed; dice size (D4…D100) matches row count; equal probability per entry |
| `test_list_type_mapping.py` | Property test | Every canonical dice size maps correctly; non-dice lengths fall back to `WEIGHTED` |
| `test_end_to_end.py` | Full script run | `inputs/` scanning works; one `.hllib` per source file; bundle contains `meta.hlmeta` and the book XML |

---

## Extending

* **Edge cases** – add Hypothesis strategies for Unicode text or very large tables.  
* **CLI flags** – Refactor `hydra_convert.py` to expose a `main(in_dir, out_dir)` function and wire `argparse`; tests then call that directly instead of changing directories.  
* **CI** – Hook `pytest` into GitHub Actions to fail fast when a table or converter change breaks something.

---

## License

None

---

## Credits

*Example data from Matt Davids’ “Book of Random Tables” series*  
*Hydra Lists by Lambda Dice*  
*Converter & tests by **YOUR-TEAM-NAME***
