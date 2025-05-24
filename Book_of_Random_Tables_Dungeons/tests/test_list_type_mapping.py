import textwrap
import pytest
import hydra_convert

CASES = [
    (4,  "D4"),  (6,  "D6"),  (8,  "D8"),  (10, "D10"),
    (12, "D12"), (20, "D20"), (100, "D100"),
    (7,  "WEIGHTED"),          # fall-through branch
]

@pytest.mark.parametrize("rows,expected", CASES)
def test_mapping(tmp_path, rows, expected):
    body = "\n".join(str(i) for i in range(rows))
    txt  = tmp_path / "table.txt"
    txt.write_text(f"Book\n=List\n{body}\n", encoding="utf8")

    _, book_xml, _ = hydra_convert.make_book(txt)
    ttype = book_xml.findtext("./TextList/TextList-Type")
    assert ttype == expected
