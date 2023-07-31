import subprocess
import mysql.connector    
def database_connection():
    ssh_config = {
        'ssh_host': '172.150.0.76',
        'ssh_port': 22,
        'ssh_username': 'c0058',
        'ssh_password': 'KSEI@fvascsc@123',
        'ssh_keyfile': 'C:\scapia\CORN_JOB\job\c0058.ppk'
    }

        # msql
    mysql_config = {
        'db_host': '172.184.21.38',
        'db_port': 2201,
        'db_user': 'c0058',
        'db_password': 'KSEI@fvascsc@123',
        'db_database': 'cards',
    }
    # Establish the SSH tunnel using plink.exe
    plink_command = [
        'plink.exe',
        '-ssh',
        '-N',  # Disable the interactive SSH session (no shell)
        '-i', ssh_config['ssh_keyfile'],
        '-L', f'{mysql_config["db_port"]}:{mysql_config["db_host"]}:{mysql_config["db_port"]}',
        f'{ssh_config["ssh_username"]}@{ssh_config["ssh_host"]}',
        '-P', str(ssh_config['ssh_port']),  # Convert the port to a string
    ]
    subprocess.Popen(plink_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # Connect to the MySQL server through the SSH tunnel
    connection = mysql.connector.connect(
        host='127.0.0.1',  # Localhost because the tunnel is created
        port=mysql_config['db_port'],
        user=mysql_config['db_user'],
        password=mysql_config['db_password'],
        database=mysql_config['db_database'],
    )

    # Create a cursor
    cursor = connection.cursor()
    return [cursor, connection]