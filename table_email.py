from datetime import date
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

password="putnqjmtyqyegnjs"


filename='book_1.xlsx'
pd.set_option('colheader_justify', 'center')

smtp_port = 587
smtp_server = "smtp.gmail.com"

def read_excel_data(filename):
    # Read data from the Excel file using pandas
    df = pd.read_excel(filename)
    numeric_columns = df.select_dtypes(include=[float,int]).columns
    df[numeric_columns] = df[numeric_columns].astype(float)
    
    df_cleaned = df.applymap(lambda x: x.strip().replace('\n', '') if isinstance(x, str) else x)
    dfna = df_cleaned.fillna('-')
    df_cleaned.columns = dfna.columns.str.replace('Unnamed:', '-')
    table_html = dfna.to_html(index=False)
    styles_table = table_html.replace('<table border="1" class="dataframe">', '<table  style="border-collapse: collapse; border:1px solid black">').replace(
         '<th', '<th style="border: 1px solid black; padding: 8px;"'
    ).replace('<td', '<td style="border: 1px solid black; padding: 4px;"').replace(
        '   <th style="border: 1px solid black; padding: 8px;">Current Date</th>', '<th style="border: 1px solid black; padding: 8px;" colspan="3">Current Date</th>'
    ).replace(' <th style="border: 1px solid black; padding: 8px;">MTD</th>', ' <th style="border: 1px solid black; padding: 8px;" colspan="3">MTD</th>'
    ).replace('<th style="border: 1px solid black; padding: 8px;">YTD</th>', 
    ' <th style="border: 1px solid black; padding: 8px;" colspan="3">YTD</th>').replace('<th style="border: 1px solid black; padding: 8px;">Unnamed: 10</th>', ' '
    ).replace('<th style="border: 1px solid black; padding: 8px;">Unnamed: 13</th>',' ').replace(
        '<th style="border: 1px solid black; padding: 8px;">Unnamed: 12</th>',' ').replace(
        '<th style="border: 1px solid black; padding: 8px;">Unnamed: 3</th>',' '
        ).replace('<th style="border: 1px solid black; padding: 8px;">Unnamed: 4</th>',' '
    ).replace(' <th style="border: 1px solid black; padding: 8px;">Unnamed: 6</th>',' '
    ).replace('<th style="border: 1px solid black; padding: 8px;">Unnamed: 9</th>',' '
    ).replace('<th style="border: 1px solid black; padding: 8px;">Unnamed: 7</th>',' '
    ).replace('<th style="border: 1px solid black; padding: 8px;">2023-06-01 00:00:00</th>','<th style="border: 1px solid black; padding: 8px;" colspan="3">June</th>'
    )
    return styles_table


def send_mail():
    body = """
    Daily Business Summary sheet.

    Regards,
    Shashidhar
    """

    # Creating the email message
    email_login = 'shashidhar.yellenki@saven.in'
    email_to = ['shashi.devv.1009@gmail.com']
    # cc_email = ['yellenkishashidhar@gmail.com']
    # password = 'behfmlubvzekgfyw'

    try:
        # Creating the message instance
        message = MIMEMultipart()
        message['From'] = 'sshashidhar.yellenki@saven.in'
        message['To'] = ', '.join(email_to)
        # message['Cc'] = ', '.join(cc_email)
        message['Subject'] = f'Daily report of {date.today()}'

        # Read data from the Excel file and convert it to HTML table
        styled_table = read_excel_data(filename)
        print(styled_table)
        # Adding the body of the email with the HTML table
        email_body = f"""
        {body}
        <br>
        {styled_table}
        """

        message.attach(MIMEText(email_body, 'html'))

        # Opening the attachment
        attachment = open(filename, 'rb')  # Opening the file and converting it to bytes

        attachment_pkg = MIMEBase('application', 'octet-stream')
        attachment_pkg.set_payload(attachment.read())

        # Using base64 encoding to encode the email content
        encoders.encode_base64(attachment_pkg)

       
        # message.attach(attachment_pkg)

        # Converting the whole message to a string
        text = message.as_string()

        # Connecting to the server and logging into the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_login, password)
        print("Logged into the email successfully")

        # Sending email with attachment
        recipients = email_to #+ cc_email
        server.sendmail(email_login, recipients, text)

        server.quit()
    except Exception as e:
        raise Exception(f"Something went wrong: {str(e)}")

# Call the send_mail function to send the email
# send_mail()
