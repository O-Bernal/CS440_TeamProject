# tests/test_parse_and_die.py
import os
import sys
# ─ Insert project folder onto path so hydra_convert.py is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest
from hydra_convert import parse_table, pick_die_type

# A minimal “random table” sample for unit testing
SAMPLE_TABLE = """
=== Noble’s Bedchamber Items
1. Burning letters
2. Hidden safe
3. Stuffed minotaur
"""

def test_parse_table_returns_expected_structure(tmp_path):
    # Arrange
    table_file = tmp_path / "table1.txt"
    table_file.write_text(SAMPLE_TABLE.strip(), encoding="utf-8")

    # Act
    result = parse_table(str(table_file))

    # Assert
    assert isinstance(result, dict)
    assert result["name"] == "Noble’s Bedchamber Items"
    assert result["entries"] == [
        "Burning letters",
        "Hidden safe",
        "Stuffed minotaur"
    ]

@pytest.mark.parametrize("count,expected", [
    (1,  "D4"),
    (4,  "D4"),
    (6,  "D6"),
    (20, "D20"),
    (25, "D20"),
])
def test_pick_die_type_various_counts(count, expected):
    assert pick_die_type(count) == expected
