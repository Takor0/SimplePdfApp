# SimplePdfApp

**SimplePdfApp** is a microservice for processing and generating PDF documents:

* **Split** existing PDFs by a text separator
* **Watermark** — apply text stamps at arbitrary angles
* **Report** — generate multiple reports from a PDF template and CSV data

All functionality is exposed via a REST API using **FastAPI**, with asynchronous background tasks powered by **Celery**, **RabbitMQ** as the broker, and task results stored in **Redis**.

---

## 🛠️ Technology Stack

* **Python 3.11+**
* **FastAPI** – high-performance HTTP framework
* **Uvicorn** – ASGI server implementation
* **Celery** – distributed task queue
* **RabbitMQ** – AMQP message broker
* **Redis** – result backend for Celery
* **PyPDF (pypdf)**, **PyMuPDF (fitz)**, **ReportLab** – PDF manipulation
* **Pandas** – CSV processing
* **Docker & Docker Compose** – containerization

---

## ⚙️ Features

1. **File Upload** for PDF and CSV files
2. **Split PDF**

   * Split a PDF into multiple files whenever a specified separator string appears
   * Optionally include or exclude the separator page in each chunk
   * Returns a ZIP archive of resulting splits
3. **Watermark**

   * Apply a semi-transparent text watermark at any angle
4. **Generate Report**

   * Fill placeholders (e.g. `<name>`) in a PDF template with values from CSV rows
   * One PDF per CSV row, returned as a ZIP archive
5. **Task Status**

   * Query task state (`PENDING`, `STARTED`, `SUCCESS`, `FAILURE`) and results via Redis
6. **Download Result**

   * Download completed ZIP files via a dedicated endpoint

---

## 🚀 RunningDocker Compose

```bash
git clone https://github.com/yourrepo/SimplePdfApp.git
cd SimplePdfApp
docker-compose up -d
```

## 🚀 Run api and celery

```bash
   make dev_run
```

```bash
   make dev_run_celery
```

* FastAPI docs:   `http://localhost:8000/docs`
* RabbitMQ UI:    `http://localhost:15672` (guest/guest)
* Redis server:   `localhost:6379`

---

## 📁 Working Directories

By default, uploaded files are stored in `/tmp/uploads` and task output in `/tmp/results`. These directories need to be created and writable by the application.

* `UPLOAD_DIR`: path for uploaded files (default `/tmp/uploads`)
* `RESULT_DIR`: path for task outputs (default `/tmp/results`)

---

## 🔧 Installation and Running

### 1. Set up Python environment

```bash
cd SimplePdfApp
python3.11 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```


### 2. Launch Application and Worker

In one terminal, run the API server:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

In another terminal, start the Celery worker:

```bash
celery -A src.celery_app:celery_app worker --loglevel=info
```

The API will be available at `http://localhost:8000` and background tasks will process asynchronously.

---

## 📘 API Endpoints

### Upload File

```
POST /api/upload
Content-Type: multipart/form-data
Form field: file (PDF or CSV)
Response: { "filename": "<saved_name>" }
```

### Run Task

```
POST /api/task/run
Content-Type: application/json
Request body (oneOf):
  • add_watermark:
    {
      "task_name": "add_watermark",
      "file_name": "in.pdf",
      "text": "WATERMARK",
      "color": "gray",
      "fontsize": 50
    }
  • split_pdf:
    {
      "task_name": "split_pdf",
      "file_name": "in.pdf",
      "separator": "SPLIT_HERE",
      "keep_separator": false
    }
  • generate_report:
    {
      "task_name": "generate_report",
      "file_name": "template.pdf",
      "data_file_name": "data.csv",
      "column_mapping": { "name": "NameCol", "age": "AgeCol" },
      "separator": ","
    }
Response: { "task_id": "<uuid>" }
```

### Task Status

```
GET /api/task/status/{task_id}
Response: { "task_id": "<uuid>", "status": "PENDING|STARTED|SUCCESS|FAILURE", "result"?, "error"? }
```

### Download Task Result

```python
@router.get("/download-result")
```

```
GET /api/task/download-result?file_name=<zip_name>
Response: ZIP file download (application/zip)
```

---

## 📝 License

MIT © takor0
