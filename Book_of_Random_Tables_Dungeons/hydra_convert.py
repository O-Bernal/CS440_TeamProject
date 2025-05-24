import os
#import shutil
import zipfile
from lxml import etree as ET
from lxml.builder import E
from io import BytesIO

inputs_folder = os.path.join(os.getcwd(), "inputs")
outputs_folder = os.path.join(os.getcwd(), "outputs")

if not os.path.exists(inputs_folder):
    raise ValueError("Inputs path does not exist.")

if not os.path.exists(outputs_folder):
    os.makedirs(outputs_folder)

# get all the input files
input_files = [os.path.join(inputs_folder, x) for x in os.listdir(inputs_folder) if os.path.isfile(os.path.join(inputs_folder, x))]

def make_book(file_name):
    # ingest file
    with open(file_name, "r", encoding="utf8") as f:
        lines = [x.strip() for x in f.readlines()]
    book_name = lines.pop(0)
    lists = []
    current_list = {}
    for line in lines:
        if len(line.strip()) == 0:
            continue
        elif line[0] == "=":
            if current_list != {}:
                lists.append(current_list)
            current_list = {}
            current_list["name"] = line[1:]
            current_list["entries"] = []
        else:
            current_list["entries"].append(line)
    # final append
    lists.append(current_list)
    # now we need to create the XMLs:
    meta_xml = E("Library",
             E("Version", "1.2"),
             E("Name", book_name),
             E("Author", "none"),
             E("Description", "Default"),
             E("LibIcon", "puzzle"),
             E("WorkshopId", "-1")
    )
    book_xml = E("Book",
             E("Book-Version", "1.2"),
             E("Book-Name", book_name),
             E("Book-Author", "none")             
             )
    for list in lists:
        list_length = len(list["entries"])
        list_type = None
        match list_length:
            case 4:
                list_type = "D4"
            case 6:
                list_type = "D6"
            case 8:
                list_type = "D8"
            case 10:
                list_type = "D10"
            case 12:
                list_type = "D12"
            case 20:
                list_type = "D20"
            case 100:
                list_type = "D100"
            case _:
                list_type = "WEIGHTED"
        list_xml = E("TextList",
                     E("TextList-Name", list["name"]),
                     E("TextList-Type", list_type),
                     E("TextList-Hidden", "false")
                     )        
        for entry in list["entries"]:
            item = E("Content",
                     E("Content-Text", entry),
                     E("Content-Chance", str((1 / list_length) * 100))
                     )
            list_xml.append(item)
        book_xml.append(list_xml)

    return meta_xml, book_xml, book_name

for input_file in input_files:
    file_meta_xml, file_book_xml, book_name = make_book(input_file)

    xml_header = b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\r\n'

    meta_file = xml_header + ET.tostring(file_meta_xml, pretty_print = True)
    book_file = xml_header + ET.tostring(file_book_xml, pretty_print = True)

    file_dict = {
        "meta.hlmeta": meta_file,
        book_name.replace(" ", "_") + "_none_1.2_.xml" : book_file
    }

    in_memory_zip = BytesIO()
    with zipfile.ZipFile(in_memory_zip, 'w') as zf:
        for filename, data in file_dict.items():
            zf.writestr(filename, data)
    in_memory_zip.seek(0)

    out_file = os.path.join(outputs_folder, book_name.replace(" ", "_") + ".hllib")

    with open(out_file, 'wb') as f:
        f.write(in_memory_zip.read())

    print(f"Converted book: {book_name}")

