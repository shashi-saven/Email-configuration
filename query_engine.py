from datetime import date

import openpyxl
from final.testref import excel_references
from final.table_email import send_mail
from final.connection import database_connection
# from creating_book import workbook_creation, save_workbook, write_to_sheet

workbook = openpyxl.load_workbook("book_1.xlsx")
sheet = workbook.active
def query_mysql_and_populate_excel():

    # Connecting to the database
    connection_detils = database_connection()
    cursor  = connection_detils[0]
    connection = connection_detils[1]

    # Loop through the references
    for key,  value in excel_references.items():
        # Determine if it is MTD or YTD reference
        # is_MTD = key.endswith("_MTD")
        # is_YTD = key.endswith("_YTD")
        # Execute the query
        try:
            cursor.execute(value['query'])
            result = cursor.fetchone()[0]
            print(key)
            print("***",value['cell_reference'], value['query'] )
            print("result",result)
        except KeyError as e:
            print(e)
            
       
        # Populate the cell with the result
        sheet[value['cell_reference']]=result

    # Save the changes to the workbook
    workbook.save("book_1.xlsx")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Completed quering the queries and staretd sending the email")
  
    send_mail()
    print("Completed...")

# Call the function to execute the query and populate the Excel file
query_mysql_and_populate_excel()



