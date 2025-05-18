import io
import shutil
import zipfile

import fitz
import pandas as pd
from pypdf import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas

from src.config import RESULTS_DIR, UPLOAD_DIR
from src.celery_app import celery_app
from src.utils.file import store_zip
from src.utils.pdf import (
    get_uploaded_file_reader,
    render_pages,
    find_doc_placeholders_styles,
)


@celery_app.task(name="add_watermark")
def add_watermark(
    file_name: str, text: str, color: str = "gray", fontsize: int = 50
) -> str:
    """
    Adds a watermark to a PDF file.

    :param file_name: name of the file to be watermarked
    :param text
    :param color
    :param fontsize: size of the watermark text
    :return: name of the watermarked file
    """
    output_file_name = f"watermarked_{file_name}"
    watermarked_path = RESULTS_DIR / output_file_name

    reader = get_uploaded_file_reader(file_name)

    first_page = reader.pages[0]
    media_box = first_page.mediabox
    width, height = float(media_box.width), float(media_box.height)

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))

    c.setFont("Helvetica", fontsize)
    c.setFillColor(color, alpha=0.3)

    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()

    packet.seek(0)
    watermark_pdf = PdfReader(packet)
    watermark_page = watermark_pdf.pages[0]

    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    writer.write(watermarked_path)

    return output_file_name


@celery_app.task(name="split_pdf")
def split_pdf(file_name: str, separator: str, keep_separator: bool = False):
    """
    Splits a PDF file into multiple files based on a separator.

    :param file_name: name of the file to be split
    :param separator: page number to split the PDF at
    :param keep_separator: whether to keep the separator page in the split files
    :return: list of names of the split files
    """

    reader = get_uploaded_file_reader(file_name)
    group_pages: list[PageObject] = []
    group_index = 0
    result_dir = RESULTS_DIR / file_name.replace(".pdf", "_split")
    zip_path = RESULTS_DIR / f"{result_dir}.zip"

    page_number = reader.get_num_pages()
    for idx, page in enumerate(reader.pages):
        group_pages.append(page)
        is_sep = separator in page.extract_text()
        if is_sep or idx == page_number - 1:
            if not keep_separator and is_sep:
                group_pages.pop()
            render_pages(
                group_pages,
                result_dir,
                file_name.replace(".pdf", f"_{group_index}.pdf"),
            )
            group_pages.clear()
            group_index += 1

    shutil.rmtree(result_dir)
    store_zip(result_dir, zip_path)

    return zip_path.name


@celery_app.task(name="generate_report")
def generate_report(
    file_name: str,
    data_file_name: str,
    column_mapping: dict[str, str],
    separator: str = ",",
) -> list[str]:
    tpl_path = UPLOAD_DIR / file_name
    csv_path = UPLOAD_DIR / data_file_name
    result_dir = RESULTS_DIR / f"{tpl_path.stem}_reports"
    result_dir.mkdir(parents=True, exist_ok=True)
    zip_path = RESULTS_DIR / f"{result_dir}.zip"

    df = pd.read_csv(csv_path, sep=separator, dtype=str).fillna("")
    doc = fitz.open(tpl_path)
    placeholders_styles_per_page = find_doc_placeholders_styles(
        doc, list(column_mapping.keys())
    )

    for idx, row in df.iterrows():
        doc = fitz.open(tpl_path)
        for num_page, page in enumerate(doc):
            placeholder_styles = placeholders_styles_per_page.get(num_page, {})
            for placeholder, col_name in column_mapping.items():
                style = placeholder_styles.get(placeholder)
                if not style:
                    continue
                rects = page.search_for(placeholder)
                for r in rects:
                    page.draw_rect(r, color=(1, 1, 1), fill=(1, 1, 1))

                    value = str(row.get(col_name, ""))
                    font_size = style["size"]
                    text_height = font_size
                    insert_point = (r.x0, r.y0 + text_height)
                    page.insert_text(
                        insert_point,
                        value,
                        fontname="helv",
                        fontsize=font_size,
                        color=style["color"],
                    )

        out_path = result_dir / f"{tpl_path.stem}_{idx+1}.pdf"
        doc.save(out_path)
        doc.close()

    store_zip(result_dir, zip_path)
    shutil.rmtree(result_dir)
    return zip_path.name
