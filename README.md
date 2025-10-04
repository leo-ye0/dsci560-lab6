# DSCI 560 Lab 6 - Wells Data Collection and Visualization

Complete pipeline for collecting, processing, and visualizing oil and gas wells data.

## Part 1: Data Collection and Database Setup

### Features
- PDF text extraction from well stimulation reports
- Web scraping of well information from online databases
- MySQL database creation and data import
- Data parsing and cleaning

### Setup
```bash
cd part1
pip install -r requirements.txt
python setup_db.py
python scraper.py
python parser.py
python upload_csv.py
```

### Files
- `pdf_to_text.py` - Extract text from PDF files
- `scraper.py` - Scrape well data from web sources
- `parser.py` - Parse stimulation data from text files
- `setup_db.py` - Create MySQL database and tables
- `upload_csv.py` - Import CSV data to database
- `database.sql` - Database schema

## Part 2: Web Visualization

### Features
- Interactive map using OpenLayers
- Well locations displayed as colored markers:
  - Green: Active wells
  - Red: Inactive wells
  - Gray: Abandoned/Plugged wells
- Detailed popups with well, production, and stimulation data
- Touchpad zoom support

### Quick Setup
```bash
cd part2
./setup.sh
```

### Development Server
```bash
cd part2
php -S localhost:8000
```

### Files
- `index.html` - Main web application
- `app.js` - JavaScript map functionality
- `demo.html` - Demo with sample data
- `api/` - PHP endpoints for database access

## Complete Setup Instructions

1. **Setup Part 1 (Database):**
   ```bash
   cd part1
   pip install -r requirements.txt
   python setup_db.py
   python scraper.py
   python parser.py
   python upload_csv.py
   ```

2. **Setup Part 2 (Web App):**
   ```bash
   cd part2
   # Update database credentials in api/config.php
   ./setup.sh
   ```

3. **Access Application:**
   - Production: `http://localhost/wells/`
   - Development: `http://localhost:8000`

## Technologies Used
- **Data Processing**: Python, BeautifulSoup, Pandas
- **Database**: MySQL
- **Web Frontend**: HTML5, CSS3, JavaScript, OpenLayers
- **Web Backend**: PHP, Apache