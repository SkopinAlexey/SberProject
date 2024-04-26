import fitz
import re
import pandas as pd
from typing import List, Dict


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


def make_dict(text) -> Dict:
    pattern4 = re.compile(r"^(?!.*\b\d{1,2}\.\d{1,2}\.\d{4}\b)\d+\.\d+\.\d+(\.\d+(\.\d+(\.\d+)?)?)?$")
    dict = {}

    current_key = "0"
    content = ""

    for element in text:
        if pattern4.search(element):
            prev_key = current_key
            current_key = element
            i = 1
            while prev_key in dict.keys():
                i += 1
                prev_key = f"{prev_key}({i})"
            dict[prev_key] = content
            content = ""
        else:
            content += element
    i = 0
    while current_key in dict.keys():
        i += 1
        current_key = f"{current_key}({i})"
    dict[current_key] = content
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
    data_frame.to_excel(f"result.xlsx")
