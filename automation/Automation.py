import os,csv,sqlite3,pyodbc
def get_single_filename(folder_path):
    files = os.listdir(folder_path)

    if len(files) >0:  # Only one file in the folder
        return files
    else:
        raise ValueError("Folder does not contain a single file.")

# # Usage example
folder_path = "F:\\python\\automation"  # Replace with the actual folder path
try:
    filenames = get_single_filename(folder_path)
except ValueError as e:
    print(str(e))

if filenames !="Folder does not contain a single file.":
    for filename in filenames:
        def convert_to_csv(filename, output_file):
            input=folder_path+f'//{filename}'
            with open(input, 'r',encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='|')
                data = list(reader)
            output=folder_path+f'//{output_file}'
            with open(output, 'w', newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)

        # Usage example
        output_file_temp = filename.find('.')
        output_file =  filename[:output_file_temp] +'.csv' # Replace with your desired output file name
        convert_to_csv(filename, output_file)
else:
    print('No file')
csv_files = os.listdir(folder_path)
for csv_file in csv_files :
    if '.csv' in csv_file:
        def create_table_from_csv(csv_file):
            # Extract table name from the CSV file name
            table_name = csv_file.split('.')[0]

            # Connect to the SQLite database
            # conn = sqlite3.connect('master.db')  # Replace 'database.db' with your desired database name
            # cursor = conn.cursor()

            server = '(localdb)\manish'
            database = 'manish'
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};'
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            # Create table with the same name as the CSV file
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

            # Read CSV file and create table columns
            with open(folder_path+f'//{csv_file}', 'r',encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                # print(header)
                for column_name in header:
                    column_name=column_name.replace(' ','_')
                    column_name=column_name.replace('.','')
                    column_name=column_name.replace('-','')
                    
                    create_table_query += f"{column_name} TEXT,"
                create_table_query = create_table_query[:-1]  # Remove the last comma
                create_table_query += ");"
            # print(create_table_query)
            try:
                cursor.execute(create_table_query)
                # connection.commit()
                print("Table created successfully!")
            except Exception as e:
                print("Error:", str(e))
                connection.rollback()

            # Insert data from the CSV file into the table
            with open(folder_path+f'//{csv_file}', 'r',encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    values = tuple(row.values())
                    placeholders = ', '.join('?' * len(values))
                    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                    # print(insert_query)
                    cursor.execute(insert_query, values)
            # res=cursor.execute(f'select * from {table_name}')
            # rows = cursor.fetchall()
            # for i in rows:
            #     print(i)
            ##Commit changes and close the connection
            connection.commit()
            connection.close()
        create_table_from_csv(csv_file)

# csv_file = output_file  # Replace with the actual CSV file name
# 