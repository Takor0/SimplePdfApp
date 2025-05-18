import zipfile
from pathlib import Path


def store_zip(dir_path: Path, zip_path: Path) -> str:
    """
    Store a zip file in the directory.

    :param zip_path: path to the zip file
    :param dir_path: path to the directory to be zipped
    :return: name of the stored zip file
    """
    zip_path.unlink(missing_ok=True)
    with zipfile.ZipFile(zip_path, "w") as zip_file:
        for file in dir_path.iterdir():
            zip_file.write(file, file.name)
    return zip_path.name
