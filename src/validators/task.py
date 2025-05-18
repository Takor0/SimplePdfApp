from pydantic import BaseModel, field_validator
from typing import Literal, Union

from werkzeug.utils import secure_filename


class FileTaskBase(BaseModel):
    file_name: str

    @field_validator("file_name", mode="before")
    def _sanitize_filename(cls, v: str) -> str:
        return secure_filename(v)


class AddWatermarkParams(FileTaskBase):
    task_name: Literal["add_watermark"]
    text: str
    color: str = "gray"
    fontsize: int = 50


class SplitPdf(FileTaskBase):
    task_name: Literal["split_pdf"]
    separator: str
    keep_separator: bool = False


class GenerateReport(FileTaskBase):
    @field_validator("data_file_name", mode="before")
    def _sanitize_filename(cls, v: str) -> str:
        return secure_filename(v)

    task_name: Literal["generate_report"]
    data_file_name: str
    column_mapping: dict[str, str]
    separator: str = ","


TaskRequestModel = Union[AddWatermarkParams, SplitPdf, GenerateReport]
