import os
import re
import json
import pandas as pd
import fitz
import pytesseract
from PIL import Image
import pdfplumber
import mysql.connector


class Patterns:
    api_no: str = (
        r"(?:\b\d{2}-\d{3}-\d{5}\b)|"
        r"(?:\b\d{2} - \d{3} - \d{5}\b)|"
        r"(?:^API(?:\s)?#:(?:\s)?\d{10}$)|"
        r"(?:API(?:\s+)?\d{10})"
    )
    operator = r"Well Operator : (.*?)\n"
    well_name = r"Well Name\s*:\s*(.*)\n"
    job_id = r"\bJob (\d+)\b"
    job_type = r"Type of Incident : (.*?)\n"
    county = r"County : (.*?)\n"
    latitude = r"(\d+°\d+\'\d+\.\d+\"[NS])"
    longitude = r"(\d+°\d+\'\d+\.\d+\"[EW])"
    datum = r"Vertical Datum to DDZ\s+([\d.]+ ft)"

    date_simulated = r"Date Stimulated\s*\n\s*(\d{1,2}/\d{1,2}/\d{4})"
    formation = r"Stimulated Formation\s*\n\s*([^\n]+)"
    top_bottom_stimulation_stages = (
        r"Top \(Ft\)\s*Bottom \(Ft\)\s*Stimulation Stages\n\s*(\d+)\s+(\d+)\s+(\d+)"
    )
    psi = r"Maximum Treatment Pressure \(PSI\)\s*\n\s*(\d+)"
    lbs = r"Lbs Proppant\s*\n\s*(\d+)"
    type_treatment = r"Type Treatment\s*\n\s*([^\n]+)"
    volume = r"Volume Units\s*\n(\d+)\s*(\w+)"
    max_treatment_rate = r"Maximum Treatment Rate \(BBLS/Min\)\s*\n\s*(\d+(?:\.\d+)?)"


def extract_text_from_pdf(pdf_path: str) -> str:
    text_all = ""

    # 1. pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_all += t + "\n"
    except Exception as e:
        print(f"[pdfplumber failed: {pdf_path}] {e}")

    # 2. fitz
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf.load_page(page_num)
                t = page.get_text("text")
                if t:
                    text_all += t + "\n"
    except Exception as e:
        print(f"[fitz failed: {pdf_path}] {e}")

    # 3. pytesseract OCR
    if not text_all.strip():
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                t = pytesseract.image_to_string(img, lang="eng")
                if t:
                    text_all += t + "\n"

    return text_all.strip()


def find_api_no(text):
    api_id = set(re.findall(Patterns.api_no, text))
    api_id = [re.sub(r"[^\d-]", "", id) for id in api_id]

    api_id_final_pattern = r"(\d{2})(\d{3})(\d{5})"
    for i in range(len(api_id)):
        if len(api_id[i]) != 12:
            match = re.search(api_id_final_pattern, api_id[i])
            if match:
                api_id[i] = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    return list(set(api_id))


def extract_data_from_text_file(filepath):
    text = extract_text_from_pdf(filepath)

    filename = os.path.basename(filepath)
    well_file_no = int(re.sub("[a-zA-Z]", "", filename.split(".")[0]))
    results = {
        "filename": filename,
        "api_no": json.dumps(find_api_no(text)),
        "well_file_no": well_file_no,
    }

    keys_encountered = set(results.keys())
    for key, pattern in dict(Patterns.__dict__).items():
        if "__" not in key:
            if key not in keys_encountered:
                results[key] = ""
                match = re.search(pattern, text)
                if match:
                    results[key] = match.group(1).strip()
                    keys_encountered.add(key)

    if results.get("job_id", "") == "":
        results["job_id"] = results["well_file_no"]

    return results


def process_folder(folder_path, output_csv="wells.csv"):
    all_records = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            filepath = os.path.join(folder_path, file)
            record = extract_data_from_text_file(filepath)
            all_records.append(record)

    df = pd.DataFrame(all_records)
    df.to_csv(output_csv, index=False)

    # upload SQL
    upload_to_sql(df)
def upload_stimulated_data(df):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",  
            database="wells_db"
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO stimulated_data (
            api_no, date_simulated, formation, top_ft, bottom_ft, stimulation_stages,
            volume, volume_units, type_treatment, lbs_proppant,
            maximum_treatment_pressure_psi, maximum_treatment_rate_bbls_per_min, details
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row.get("api_no", ""),
                row.get("date_simulated", None),
                row.get("formation", ""),
                row.get("top_ft", None),
                row.get("bottom_ft", None),
                row.get("stimulation_stages", None),
                row.get("volume", None),
                row.get("volume_units", ""),
                row.get("type_treatment", ""),
                row.get("lbs_proppant", None),
                row.get("maximum_treatment_pressure", None),
                row.get("maximum_treatment_rate", None),
                row.get("details", "")
            ))

        conn.commit()
        print(f"uploaded {len(df)} stimulated_data to SQL")
    except Exception as e:
        print(f"unable to upload: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    process_folder("pdfs", "stimulated_data.csv")
