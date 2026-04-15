# AI Affiliate Idea Generator

App ini ialah projek Python + Streamlit untuk jana idea kandungan affiliate TikTok menggunakan AI.

User hanya perlu masukkan nama produk, pilih bahasa, kemudian app akan hasilkan:

- brand
- ciri utama produk
- problem statement
- 3 idea video TikTok
- hook
- call to action

## Keperluan

- Python 3.10+ disyorkan
- `OPENROUTER_API_KEY`

## Install

Buka PowerShell dalam folder projek:

```powershell
cd C:\Users\User\OneDrive\Documents\affiliate-ai
```

Install dependency:

```powershell
python -m pip install -r requirements.txt
```

## Setup `.env`

Cipta fail `.env` di root projek dan letak API key anda:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Cara Run

Jalankan app dengan command berikut:

```powershell
python -m streamlit run app.py
```

Selepas itu buka browser di:

```text
http://localhost:8501
```

## Cara Guna

1. Masukkan nama produk.
2. Pilih bahasa sama ada Bahasa Melayu atau English.
3. Klik `Generate Idea`.
4. Muat turun hasil jika perlu.

## Struktur Projek

```text
affiliate-ai/
|-- app.py
|-- ai_engine.py
|-- requirements.txt
|-- .env
```

## Fail Utama

- `app.py` mengandungi UI Streamlit.
- `ai_engine.py` mengandungi logik panggilan API OpenRouter.
- `requirements.txt` senarai package Python yang diperlukan.

## Troubleshooting

Jika `python -m streamlit run app.py` tidak berjaya:

1. Pastikan Python sudah dipasang.
2. Pastikan dependency sudah di-install:

```powershell
python -m pip install -r requirements.txt
```

3. Pastikan `.env` wujud dan `OPENROUTER_API_KEY` betul.
4. Jika port `8501` sedang digunakan, cuba:

```powershell
python -m streamlit run app.py --server.port 8502
```

## Nota

Folder `venv` dalam repo ini mungkin belum disetup sepenuhnya. Jika mahu guna virtual environment, anda boleh buat semula:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
