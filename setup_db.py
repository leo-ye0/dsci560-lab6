import mysql.connector

def setup_wells_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='D4o9n1g7!'
        )
        
        cursor = connection.cursor()

        # read sql
        with open('database.sql', 'r') as f:
            sql_content = f.read()

        # Split and execute each command
        commands = sql_content.split(';')
        for command in commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except Exception as cmd_err:
                    print(f"⚠️ Failed executing: {command}\n   Error: {cmd_err}")

        connection.commit()
        print("Wells database setup completed successfully!")

    except Exception as e:
        print(f"Error setting up wells database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_wells_database()
