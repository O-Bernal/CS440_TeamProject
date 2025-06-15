"""
Hydra Converter
Converts plain-text random-table files into Hydra Lists library bundles (.hllib).
"""
# pylint: disable=E0611, R0911, R0914, I1101

import os
import re
import zipfile
from io import BytesIO

from lxml import etree as ET
from lxml.builder import E

# Constants
VERSION = '1.2'
AUTHOR = 'none'
INPUTS_FOLDER = "inputs"
OUTPUTS_FOLDER = "outputs"
XML_HEADER = b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\r\n'


def parse_table(file_path: str) -> dict:
    """Parse a single-table text file into {'name': table_name, 'entries': [...]}."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    table_name = ''
    entries = []
    for line in lines:
        if line.startswith('='):
            table_name = line.lstrip('=').strip()
        else:
            entries.append(re.sub(r'^\d+\.\s*', '', line))
    return {'name': table_name, 'entries': entries}


def parse_book(file_path: str) -> dict:
    """Parse a multi-table file: first line is book_name, '=' lines start new tables."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        return {'book_name': '', 'tables': []}
    book_name = lines[0]
    tables = []
    current = None
    for line in lines[1:]:
        if line.startswith('='):
            current = {'name': line.lstrip('=').strip(), 'entries': []}
            tables.append(current)
        elif current is not None:
            current['entries'].append(re.sub(r'^\d+\.\s*', '', line))
    return {'book_name': book_name, 'tables': tables}


def pick_die_type(count: int) -> str:
    """Exact-match for canonical sizes; <4→D4; >20→D20; else WEIGHTED."""
    mapping = {4: 'D4', 6: 'D6', 8: 'D8', 10: 'D10', 12: 'D12', 20: 'D20', 100: 'D100'}
    if count in mapping:
        return mapping[count]
    if count < 4:
        return 'D4'
    if count > 20:
        return 'D20'
    return 'WEIGHTED'


def make_book(file_path: str) -> tuple:
    """Generate meta, book XML elements and base name from a table file."""
    parsed = parse_book(file_path)
    book_name = parsed['book_name']
    tables = parsed['tables']

    # Build metadata XML
    meta_xml = E(
        'Library',
        E('Version', VERSION),
        E('Name', book_name),
        E('Author', AUTHOR),
        E('Description', 'Default'),
        E('LibIcon', 'puzzle'),
        E('WorkshopId', '-1')
    )

    # Build book XML
    book_xml = E(
        'Book',
        E('Book-Version', VERSION),
        E('Book-Name', book_name),
        E('Book-Author', AUTHOR)
    )

    # Append each table
    for tbl in tables:
        die_type = pick_die_type(len(tbl['entries']))
        text_list = E(
            'TextList',
            E('TextList-Name', tbl['name']),
            E('TextList-Type', die_type),
            E('TextList-Hidden', 'false')
        )
        for entry in tbl['entries']:
            chance = str((1 / len(tbl['entries'])) * 100)
            content = E(
                'Content',
                E('Content-Text', entry),
                E('Content-Chance', chance)
            )
            text_list.append(content)
        book_xml.append(text_list)

    return meta_xml, book_xml, book_name


def main(input_dir: str = INPUTS_FOLDER, output_dir: str = OUTPUTS_FOLDER) -> None:
    """Process all .txt files in input_dir into .hllib bundles in output_dir."""
    cwd = os.getcwd()
    in_path = os.path.join(cwd, input_dir)
    out_path = os.path.join(cwd, output_dir)

    if not os.path.isdir(in_path):
        raise FileNotFoundError(f"Input directory does not exist: {in_path}")
    os.makedirs(out_path, exist_ok=True)

    for fname in os.listdir(in_path):
        if not fname.lower().endswith('.txt'):
            continue
        full_path = os.path.join(in_path, fname)
        meta_xml, book_xml, book_name = make_book(full_path)

        # Create in-memory .hllib archive
        archive = BytesIO()
        with zipfile.ZipFile(archive, 'w') as zf:
            meta_bytes = XML_HEADER + ET.tostring(meta_xml, pretty_print=True)
            book_bytes = XML_HEADER + ET.tostring(book_xml, pretty_print=True)
            zf.writestr('meta.hlmeta', meta_bytes)
            xml_filename = f"{book_name.replace(' ', '_')}_{AUTHOR}_{VERSION}_.xml"
            zf.writestr(xml_filename, book_bytes)
        archive.seek(0)

        # Write .hllib
        hllib_name = f"{book_name.replace(' ', '_')}.hllib"
        with open(os.path.join(out_path, hllib_name), 'wb') as f_out:
            f_out.write(archive.read())
        print(f"Converted book: {book_name}")

if __name__ == "__main__":
    main()
