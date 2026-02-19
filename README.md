# PDF Extractor + Web Scraper + ETL

Este proyecto es una demostración de un pipeline ETL (Extract, Transform, Load) diseñado para procesar información de diversas fuentes. Combina técnicas de web scraping para recolectar datos de internet y herramientas de extracción de texto y tablas de documentos PDF. Una vez extraídos, los datos son limpiados, estructurados y finalmente cargados en formatos accesibles como CSV y texto plano. Es una solución versátil para la automatización de la recolección y preparación de datos.




![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-green?style=for-the-badge)
![pdfplumber](https://img.shields.io/badge/pdfplumber-2.0-blue?style=for-the-badge)

## 🎯 Objetivo
Demostrar capacidad real en:
- Web scraping con XPath/CSS + BeautifulSoup + lxml
- Extracción avanzada de texto y tablas de PDFs
- Proceso ETL completo (Extract → Transform → Load)
- Buenas prácticas (estructura de proyecto, README claro, requirements, logging)

## 🛠 Tecnologías utilizadas
- Python 3.11
- BeautifulSoup4 + lxml (para scraping)
- pdfplumber (para PDFs – más fácil y potente que pdfminer)
- Requests
- Pandas (limpieza ETL)
- JSON + CSV (output)

## 📁 Estructura del proyecto

```
unumbio-demo-pdf-scraping-etl/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── init.py
│   ├── scraper.py          # Web scraping demo
│   ├── pdf_extractor.py    # Extracción de PDFs
│   └── etl_pipeline.py     # Proceso ETL completo
├── data/
│   ├── input/
│   │   ├── sample.pdf      # ← Descarga aquí tu PDF de prueba
│   │   └── sample_url.txt  # URLs a scrapear
│   └── output/
│       ├── scraped_data.json
│       ├── extracted_text.txt
│       └── cleaned_data.csv
└── logs/
└── app.log
```


## 🚀 Instalación 

```bash
git clone https://github.com/TU-USUARIO/unumbio-demo-pdf-scraping-etl.git
cd unumbio-demo-pdf-scraping-etl
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

# requirements.txt
```env
requests==2.32.3
beautifulsoup4==4.12.3
lxml==5.3.0
pdfplumber==0.11.0
pandas==2.2.3
```

# ▶️ Cómo ejecutar
```python
# 1. Scraping demo
python src/scraper.py

# 2. PDF extractor demo
python src/pdf_extractor.py

# 3. ETL completo (scraping → limpieza → guardado)
python src/etl_pipeline.py
```

# 📸 Resultados esperados

Carpeta data/output/ con archivos JSON, TXT y CSV limpios.   
Logs claros en logs/app.log.
