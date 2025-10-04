# DSCI 560 Lab 6 - Well Data Processing System

## Overview
A comprehensive system for processing oil and gas well data from PDFs and text files, with web scraping capabilities and MySQL database integration.

## Project Structure
```
dsci560-lab6/
├── part1/
│   ├── parser.py           # Text extraction from PDFs/text files
│   ├── scraper.py          # Web scraping for well production data
│   ├── pdf_to_text.py      # PDF to text conversion using PyMuPDF + OCR
│   ├── upload_csv.py       # CSV to MySQL database upload
│   ├── setup_db.py         # Database setup script
│   └── database.sql        # Database schema
└── data/
    ├── text_files/         # Extracted text files
    ├── scraped_data.csv    # Scraped well information
    └── stimulated_data.csv # Well stimulation data
```

## Features

### 1. PDF/Text Processing (`parser.py`)
- Extracts well data from text files
- Supports multiple text layouts and formats
- Handles Figure 1 (Well Data) and Figure 2 (Stimulation Data)
- Outputs structured CSV data

### 2. PDF to Text Conversion (`pdf_to_text.py`)
- Uses PyMuPDF (fitz) for efficient PDF text extraction
- Falls back to OCR using Pytesseract for image-based PDFs
- Batch processes multiple PDFs

### 3. Web Scraping (`scraper.py`)
- Scrapes well production data from drillingedge.com
- Separates oil and gas production values
- Extracts well status, type, location, and coordinates

### 4. Database Integration
- MySQL database with two main tables:
  - `wells`: Well information and production data
  - `stimulated_data`: Well stimulation details
- Automated table creation and data upload

## Database Schema

### Wells Table
```sql
CREATE TABLE wells (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    api_no VARCHAR(50),
    well_status VARCHAR(100),
    well_type VARCHAR(100),
    closest_city VARCHAR(255),
    county VARCHAR(255),
    lat_long VARCHAR(100),
    oil_prod DECIMAL(10,2),
    gas_prod DECIMAL(10,2)
);
```

### Stimulated Data Table
```sql
CREATE TABLE stimulated_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id VARCHAR(50),
    api_no VARCHAR(50),
    date_stimulated DATE,
    stimulated_formation TEXT,
    top_ft INT,
    bottom_ft INT,
    stimulation_stages INT,
    volume BIGINT,
    volume_units VARCHAR(50),
    type_treatment TEXT,
    lbs_proppant BIGINT,
    maximum_treatment_pressure_psi INT,
    maximum_treatment_rate_bbls_per_min DECIMAL(10,2)
);
```

## Usage

### 1. Setup Database
```bash
cd part1
python setup_db.py
```

### 2. Convert PDFs to Text (if needed)
```bash
python pdf_to_text.py
```

### 3. Extract Data from Text Files
```bash
python parser.py
```

### 4. Scrape Well Production Data
```bash
python scraper.py
```

### 5. Upload Data to Database
```bash
python upload_csv.py
```

## Dependencies
```
pandas
mysql-connector-python
requests
beautifulsoup4
PyMuPDF (fitz)
pytesseract
Pillow
pdfplumber
```

## Data Sources
- **Text Files**: Well reports and stimulation data
- **Web Scraping**: drillingedge.com for production data
- **Output**: CSV files and MySQL database

## Key Data Fields

### Well Information (Figure 1)
- API#, Longitude, Latitude
- Well Name & Number, Address/Location
- Operator, Job Type, County, Datum

### Stimulation Data (Figure 2)
- Date Stimulated, Formation, Top/Bottom Ft
- Stimulation Stages, Volume, Type Treatment
- Lbs Proppant, Max Pressure/Rate
- Proppant breakdown details

### Production Data (Scraped)
- Oil production (barrels)
- Gas production (MCF)
- Well status and type
- Geographic coordinates

## Notes
- Handles multiple text file layouts automatically
- Separates oil and gas production for better analysis
- Includes data validation and error handling
- Supports batch processing of multiple files