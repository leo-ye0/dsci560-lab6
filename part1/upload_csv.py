import pandas as pd
import mysql.connector
from datetime import datetime

def upload_csv_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="password",
            database="wells_db"
        )
        cursor = conn.cursor()
        
        # Drop and recreate tables
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DROP TABLE IF EXISTS wells")
        cursor.execute("DROP TABLE IF EXISTS stimulated_data")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Create wells table
        cursor.execute("""
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
        )
        """)
        
        # Create stimulated_data table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stimulated_data (
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
        )
        """)
        
        # Upload scraped_data.csv to wells table
        try:
            scraped_df = pd.read_csv("../data/scraped_data.csv")
            for _, row in scraped_df.iterrows():
                cursor.execute("""
                INSERT INTO wells (
                    name, api_no, well_status, well_type, closest_city,
                    county, lat_long, oil_prod, gas_prod
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, tuple(row.where(pd.notnull(row), None)))
            print(f"Uploaded {len(scraped_df)} records to wells")
        except FileNotFoundError:
            print("scraped_data.csv not found")
        
        # Upload stimulated_data.csv
        try:
            stim_df = pd.read_csv("../data/stimulated_data.csv")
            for _, row in stim_df.iterrows():
                # Convert date format
                date_val = row['date_stimulated']
                if pd.notnull(date_val) and date_val:
                    try:
                        date_val = datetime.strptime(str(date_val), "%m-%d-%y").strftime("%Y-%m-%d")
                    except:
                        try:
                            date_val = datetime.strptime(str(date_val), "%m/%d/%Y").strftime("%Y-%m-%d")
                        except:
                            date_val = None
                else:
                    date_val = None
                
                values = list(row.where(pd.notnull(row), None))
                values[2] = date_val  # Replace date_stimulated with converted value
                
                cursor.execute("""
                INSERT INTO stimulated_data (
                    file_id, api_no, date_stimulated, stimulated_formation, top_ft, bottom_ft,
                    stimulation_stages, volume, volume_units, type_treatment, lbs_proppant,
                    maximum_treatment_pressure_psi, maximum_treatment_rate_bbls_per_min
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, tuple(values))
            print(f"Uploaded {len(stim_df)} records to stimulated_data")
        except FileNotFoundError:
            print("stimulated_data.csv not found")
        
        conn.commit()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    upload_csv_to_mysql()