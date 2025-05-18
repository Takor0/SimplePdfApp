# SimplePdfApp

**SimplePdfApp** to mikrousługa do przetwarzania i generowania dokumentów PDF:  
- **Split** istniejących PDF-ów według separatora,  
- **Watermark** — nakładanie tekstowych stempli,  
- **Report** — generowanie wielu raportów z szablonu PDF i danych z CSV.  

Wszystko wystawione jako REST API za pomocą **FastAPI**, zadania asynchronicznie odpalane przez **Celery** z kolejką **RabbitMQ** i wynikami trzymanymi w **Redis**.  

---

## 🛠️ Stack technologiczny

- **Python 3.11+**  
- **FastAPI** – szybki framework HTTP  
- **Uvicorn** – ASGI server  
- **Celery** – kolejka zadań  
- **RabbitMQ** – broker AMQP  
- **Redis** – result backend  
- **PyPDF (pypdf)**, **PyMuPDF (fitz)**, **ReportLab** – manipulacja PDF  
- **Pandas** – czytanie CSV  
- **Docker & Docker Compose** – konteneryzacja  

---

## ⚙️ Funkcjonalności

1. **Upload** plików PDF / CSV  
2. **Split PDF**  
   - dzielenie pliku na podpliki według separatora (fraza w tekście),  
   - opcja zachowania lub odrzucenia strony separatora,  
   - wynik ZIP z kawałkami.  
3. **Watermark**  
   - nakładanie półprzezroczystego tekstu (stempla) pod dowolnym kątem,  
   - w pamięci (bez plików tymczasowych).  
4. **Generate Report**  
   - szablon PDF z placeholderami `<key>`,  
   - CSV z wieloma wierszami i mapowaniem kolumn → placeholder,  
   - osobny PDF dla każdego wiersza + wynikowy ZIP.  
5. **Status zadań** – endpoint sprawdzający postęp/stany w Redis.  

---

## 🚀 Uruchomienie z Docker Compose

```bash
git clone https://github.com/yourrepo/SimplePdfApp.git
cd SimplePdfApp

# zbuduj i odpalić RabbitMQ + Redis + API + worker
docker-compose up -d
