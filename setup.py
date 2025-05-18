from setuptools import setup, find_packages

setup(
    name="SimplePdfApp",
    version="0.1.0",
    description="Minimal FastAPI + Celery service for generating PDF thumbnails",
    author="Tomasz",
    packages=find_packages(
        include=[
            "*",
        ]
    ),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "celery",
        "pypdf",
        "PyMuPDF",
        "reportlab",
        "python-multipart",
        "redis",
        "werkzeug",
        "black",
        "pandas",
    ],
    entry_points={
        # opcjonalnie: konsolowy skrót do uruchomienia API
        "console_scripts": [
            "run-pdf-api = main:app",
        ],
    },
)
