import textwrap
from pathlib import Path
from lxml import etree as ET
import hydra_convert

def test_basic_book(tmp_path):
    """A 4-entry and a 6-entry list become D4 and D6 tables with equal chances."""
    raw = textwrap.dedent("""\
        Test Book
        =Colours
        red
        green
        blue
        yellow
        =Numbers
        one
        two
        three
        four
        five
        six
    """)
    txt = tmp_path / "in.txt"
    txt.write_text(raw, encoding="utf8")

    meta_xml, book_xml, name = hydra_convert.make_book(txt)

    # Book-level metadata
    assert name == "Test Book"
    assert book_xml.findtext("Book-Name") == "Test Book"

    # Two <TextList>s with correct dice sizes
    tlists = book_xml.findall("./TextList")
    assert len(tlists) == 2
    assert tlists[0].findtext("TextList-Type") == "D4"
    assert tlists[1].findtext("TextList-Type") == "D6"

    # Chances are uniformly 25 % and 16.66 %
    chances_1 = [float(c.text) for c in tlists[0].findall("./Content/Content-Chance")]
    chances_2 = [float(c.text) for c in tlists[1].findall("./Content/Content-Chance")]
    assert all(c == 25.0 for c in chances_1)
    assert all(round(c, 2) == 16.67 for c in chances_2)
