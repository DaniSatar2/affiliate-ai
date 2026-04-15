# AI Affiliate Idea Generator

AI Affiliate Idea Generator ialah app `Streamlit` untuk menjana idea kandungan affiliate TikTok berdasarkan nama produk.

App ini menggunakan `OpenRouter` untuk menghasilkan output dalam format berstruktur seperti:

- brand
- features
- problem statement
- 3 idea video TikTok
- hook
- call to action

## Tech Stack

- Python
- Streamlit
- Requests
- python-dotenv
- OpenRouter API
- GPT-4o mini
- Dev Containers / GitHub Codespaces
- VS Code Python Extension
- VS Code Pylance

## Struktur Projek

```text
affiliate-ai/
|-- app.py
|-- ai_engine.py
|-- requirements.txt
|-- README.md
|-- .env
|-- .devcontainer/
```

## Keperluan

- Python 3.10 atau lebih baru
- API key OpenRouter

## Setup

Masuk ke folder projek:

```powershell
cd C:\Users\User\OneDrive\Documents\affiliate-ai
```

Buat virtual environment baru:

```powershell
python -m venv .venv
```

Aktifkan virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Development Environment

Repo ini juga ada konfigurasi `Dev Container` dalam `.devcontainer/devcontainer.json`.

Jika anda buka projek ini dalam:

- VS Code Dev Containers
- GitHub Codespaces

environment Python dan `Streamlit` boleh disediakan secara automatik berdasarkan konfigurasi tersebut.

## Setup `.env`

Cipta fail `.env` di root projek dan letakkan API key anda:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Cara Run

Jalankan app dengan:

```powershell
python -m streamlit run app.py
```

Kemudian buka browser di:

```text
http://localhost:8501
```

Jika port `8501` sedang digunakan:

```powershell
python -m streamlit run app.py --server.port 8502
```

## Cara Guna

1. Masukkan nama produk.
2. Pilih bahasa `Bahasa Melayu` atau `English`.
3. Klik `Generate Idea`.
4. Semak output yang dijana.
5. Muat turun hasil sebagai fail `.txt` jika perlu.

## Fail Utama

- `app.py`
  UI `Streamlit`, session state, parser output AI, history, dan download hasil.
- `ai_engine.py`
  Logik panggilan ke OpenRouter API serta error handling untuk request AI.
- `requirements.txt`
  Senarai dependency Python yang diperlukan oleh projek.

## Troubleshooting

Jika app tidak boleh start:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Jika keluar error `OPENROUTER_API_KEY tidak dijumpai`:

- pastikan fail `.env` wujud
- pastikan nama variable ialah `OPENROUTER_API_KEY`
- pastikan API key yang dimasukkan betul

Jika `venv` atau `.venv` nampak kosong:

- itu biasanya bermaksud virtual environment belum dicipta dengan sempurna
- buat semula dengan `python -m venv .venv`

Jika `git push` ditolak kerana branch diverged:

```powershell
git pull --rebase origin main
git push
```

## Nota

- Jangan commit fail `.env` ke GitHub.
- Jika output AI tidak ikut format sepenuhnya, app masih akan cuba parse dan paparkan output mentah untuk rujukan.
