from pathlib import Path

import fitz
import pymupdf
from pypdf import PdfReader, PageObject, PdfWriter

from src.config import UPLOAD_DIR


def get_uploaded_file_reader(file_name: str) -> PdfReader:
    """
    Returns a PdfReader object for the given file name.

    :param file_name: name of the file to be read
    :return: PdfReader object
    """
    uploaded_file_path = UPLOAD_DIR / file_name

    if not uploaded_file_path.exists():
        raise FileNotFoundError(f"File {uploaded_file_path} not found.")

    return PdfReader(uploaded_file_path)


def render_pages(pages: list[PageObject], path: Path, file_name: str) -> Path:
    if not path.exists():
        path.mkdir(exist_ok=True)

    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)

    out_file = path / file_name
    writer.write(out_file)

    return out_file


def find_page_placeholders_styles(page: fitz.Page, placeholders: list[str]):
    """
    :param page
    :param placeholders: placeholders to search for

    :return: dictionary of placeholder with the rectangle, font, size, and color of the placeholder
    """
    styles = {}
    td = page.get_text("dict")
    for b in td["blocks"]:
        for line in b.get("lines", []):
            for span in line.get("spans", []):
                for placeholder in placeholders:
                    if placeholder in span["text"]:
                        rect = fitz.Rect(span["bbox"])
                        font = span.get("font", "helv")
                        size = span.get("size", 12)
                        col = span.get("color", 0)
                        r = ((col >> 16) & 0xFF) / 255.0
                        g = ((col >> 8) & 0xFF) / 255.0
                        b = (col & 0xFF) / 255.0
                        styles[placeholder] = {
                            "rect": rect,
                            "font": font,
                            "size": size,
                            "color": (r, g, b),
                        }
    return styles


def find_doc_placeholders_styles(doc: pymupdf.Document, placeholders: list[str]):
    """
    :param doc
    :param placeholders: placeholders to search for

    :return: dictionary of page number with the dictionary of placeholder with the rectangle, font, size, and color of the placeholder
    """
    styles = {}
    for page_num, page in enumerate(doc):
        styles[page_num] = find_page_placeholders_styles(page, placeholders)
    return styles
