import os
from io import BytesIO
import pdfplumber

def process_pdf_local(pdf_path, out_dir="text_files"):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    filepath = os.path.join(out_dir, f"{filename}.txt")

    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(filepath):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        text_all = ""

        # pdfplumber
        try:
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_all += t + "\n"
        except Exception as e:
            print(f"[pdfplumber failed: {filename}] {e}")



        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text_all.strip())

        print(f"Saved: {filepath}")
    else:
        print(f"Skipped (already exists): {filepath}")

    return filepath


def process_all_pdfs_local(pdf_dir="pdfs", out_dir="text_files"):
    pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

    print(f" {len(pdf_files)} PDF files")
    if not pdf_files:
        print("No PDF files found")
        return

    for pdf_path in pdf_files:
        print(f"Processing {pdf_path} ...")
        process_pdf_local(pdf_path, out_dir=out_dir)

    #print(f":{out_dir}/")


if __name__ == "__main__":
    process_all_pdfs_local(pdf_dir="pdfs", out_dir="text_files")
