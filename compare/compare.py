import fitz
import re
import pandas as pd
from typing import List, Dict

from PySide6 import QtGui


def get_text_from_file(filename):
    pdf_file = fitz.open(filename)
    arr = ""
    for p in range(len(pdf_file)):
        page = pdf_file.load_page(p)
        page_text = page.get_text()
        arr += page_text
    arr = arr.replace('\u200b', '')
    text = arr.split('\n')
    return text


def add_col(texts: List[Dict], index) -> List[str]:
    res = []
    for text in texts:
        if index in text:
            res.append(text[index])
        else:
            res.append("-")
    return res


def add_key(key, content, dict):
    if key != "0":
        if key in dict.keys():
            i = 2
            while f"{key}({i})" in dict.keys():
                i += 1
            key = f"{key}({i})"
        dict[key] = content


def make_dict(text) -> Dict:
    pattern4 = re.compile(r"^(?!.*\b\d{1,2}\.\d{1,2}\.\d{4}\b)\d+\.\d+\.\d+(\.\d+(\.\d+(\.\d+)?)?)?$")
    pattern_paragraph = re.compile(r"\d+\.\d+\s")
    pattern_chapter = re.compile(r"\d{2}\s")
    dict = {}
    current_key = "0"
    content = ""
    last_paragraph = False

    for element in text:
        if pattern4.search(element):
            if not last_paragraph:
                prev_key = current_key
                current_key = element
                if prev_key != "0":
                    add_key(prev_key, content, dict)
                    content = ""
            last_paragraph = False
        elif pattern_paragraph.search(element) or pattern_chapter.search(element):
            if not last_paragraph and current_key != "0":
                prev_key = current_key
                add_key(prev_key, content, dict)
                content = ""
                current_key = "0"
            last_paragraph = True
        else:
            if current_key == "0":
                continue
            content += element
    i = 0
    while current_key in dict.keys():
        i += 1
        current_key = f"{current_key}({i})"
    dict[current_key] = content
    # for i in range(10):
    #     print()
    # for key, value in dict.items():
    #     print(key, value, "\n")
    # print("\n".join(dict.values()))
    return dict


def compare_pdfs(texts: List[Dict]):
    if len(texts) != 0:
        res = {}
        for i in texts[0]:
            first = texts[0][i]
            for index, text in enumerate(texts):
                if i in text:
                    if text[i] != first:
                        res[i] = add_col(texts, i)
                else:
                    res[i] = add_col(texts, i)

        return res


def start_compare(pdfs):
    texts = []
    for pdf in pdfs:
        text = get_text_from_file(pdf)
        texts.append(make_dict(text))
    res = compare_pdfs(texts)
    data_frame = pd.DataFrame.from_dict(res, orient='index')
    #data_frame.to_excel(f"result.xlsx")
    return data_frame
