# DSCI 560 Lab 6

## Part 1
A complete pipeline that extracts **stimulation data** from PDF files, applies OCR for scanned reports, and stores the results in a MySQL database.

## Features

- **PDF Parsing**: Extracts text from structured PDF reports using `pdfplumber` and `PyMuPDF`
- **OCR Fallback**: Uses `pytesseract` to process scanned PDFs with no embedded text
- **Pattern Matching**: Regex-based extraction of API number, operator, well name, county, etc.
- **Stimulation Data Extraction**: Parses formation, date, top/bottom depth, stages, volume, pressure, and treatment type
- **Database Storage**: MySQL integration with separate tables for wells and stimulation data

## Database Schema

### `wells` and `stimulated_data`
```sql
CREATE TABLE wells (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(100),
    api_no VARCHAR(20),
    well_file_no INT,
    operator VARCHAR(255),
    well_name VARCHAR(255),
    job_id VARCHAR(50),
    job_type VARCHAR(255),
    county VARCHAR(255),
    latitude VARCHAR(50),
    longitude VARCHAR(50),
    datum VARCHAR(50),
    well_status VARCHAR(100),
    well_type VARCHAR(100),
    closest_city VARCHAR(100)
);

CREATE TABLE stimulated_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_no VARCHAR(20),
    date_simulated DATE,
    formation VARCHAR(255),
    top_ft INT,
    bottom_ft INT,
    stimulation_stages INT,
    volume BIGINT,
    volume_units VARCHAR(50),
    type_treatment VARCHAR(100),
    lbs_proppant BIGINT,
    maximum_treatment_pressure_psi INT,
    maximum_treatment_rate_bbls_per_min DECIMAL(10,2)
);
```
## Setup
1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tesseract OCR**
   ```bash
   sudo apt install tesseract-ocr
   ```

3. **Setup Database**
   ```bash
   python setup_db.py
   ```

## Usage

### Turn PDFs to text files
```bash
python pdf_to_text.py
```
- Scans pdfs/ folder
- Outputs text files for every pdf

### Scraping from text files
```bash
python parser.py
```
- find patterns in text files
- output stimulated data into csv file and upload to SQL database

## Files

- `parser.py` - Extracts text, applies OCR, and generates CSV files
- `database.sql` - Schema for wells and stimulated_data tables
- `setup_database.py` - Initializes MySQL database and tables
- `database_setup.sql` - MySQL schema
- `requirements.txt` - Python dependencies
