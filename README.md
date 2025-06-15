# CS440 Team Project: SQA of Hydra Convert

![Coverage](https://img.shields.io/codecov/c/github/O-Bernal/CS440_TeamProject)

Hydra Convert turns plain-text random-table files into Hydra Lists library bundles (.hllib).
...

**Hydra Convert** is a small command-line utility that turns plain-text “random-table” files into **Hydra Lists** library bundles (`.hllib`).  
Hydra Lists (Steam / itch.io) is a GUI dice-roller for Game Masters: import a bundle, click the dice icon, and it rolls results instantly.

---

## Project layout
```yaml
.
├── .github/workflows/
    └── ci.yml              # GitHub Actions CI pipeline
├── Book_of_Random_Tables_Dungeons/
    ├── inputs/             # sample .txt tables (input)
    ├── outputs/            # generated .hllib bundles (output)
    ├── tests/              # automated test suite
    └── hydra_convert.py    # main converter module
├── .gitignore              # files & folders to ignore
├── pytest.ini              # pytest configuration
├── README.md               # this file
└── requirements.txt        # project dependencies
```

*(The `inputs/` and `outputs/` folders are created automatically if they don’t exist.)*

---

## Prerequisites

* **Python 3.10+**
* Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Running `hydra_convert.py` converts all `.txt` files under `inputs/` into `.hllib` bundles in `outputs/`:
```YAML
...
├── Book_of_Random_Tables_Dungeons/
    ├── inputs/
    ├── outputs/
...
```

---

## Running the tests

From the repo root:
```bash
pytest -q
```


### What the tests cover

| Test file | Description |
|-----------|---------|
| `test_end_to_end.py` | Runs the full conversion end-to-end, producing a valid `.hllib` archive in `outputs/`. |
| `test_list_type_mapping.py` | Ensures `make_book()` maps exact entry counts to canonical dice sizes or `WEIGHTED`. |
| `test_make_book.py` | Verifies multi-table files produce one `<TextList>` per section and the correct book name. |
| `test_parse_and_die.py` | Validates `parse_table()` strips numbering and `pick_die_type()` clamps/exacts correctly. |

---

## Extending
* Add CLI flags (e.g., --version, --author, or custom metadata).
* Plug in schema validation for the generated XML.
* Expand Hypothesis‐based property tests for edge-case fuzzing.
* Integrate user feedback to refine usability and error reporting.

---

## License

None. This is a class project. Feel free to adapt under your own academic/project license.

---

## Credits

*Example data from Matt Davids’ “Book of Random Tables” series Hydra Lists by Lambda Dice*

Initial Hydra_Converter by Daughtry, R.

SQA by CS440 Team 2
