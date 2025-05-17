from setuptools import setup, find_packages

setup(
    name="SimplePdfApp",
    version="0.1.0",
    description="Minimal FastAPI + Celery service for generating PDF thumbnails",
    author="Tomasz",
    packages=find_packages(include=["*",]),

    install_requires=[
        "fastapi>=0.85.0",
        "uvicorn[standard]>=0.18.0",
        "celery>=5.2.0",
        "PyMuPDF>=1.21.0"
        "python-multipart>=0.0.5",
    ],

    entry_points={
        # opcjonalnie: konsolowy skrót do uruchomienia API
        "console_scripts": [
            "run-pdf-api = main:app",
        ],
    },

)
