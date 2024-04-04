import boto3
import pymysql
from botocore.exceptions import NoCredentialsError, ClientError

def read_from_s3(bucket_name, file_key):
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        data = response['Body'].read().decode('utf-8')
        return data
    except (NoCredentialsError, ClientError) as e:
        print("Error reading from S3:", e)
        return None

def push_to_rds(data, db_endpoint, db_name, db_user, db_password):
    try:
        connection = pymysql.connect(host=db_endpoint, user=db_user, password=db_password, database=db_name)
        cursor = connection.cursor()
        # Assuming data is in a CSV format, adjust as per your data format
        rows = data.split('\n')
        for row in rows:
            if row.strip():
                values = tuple(row.split(','))  # Assuming CSV data
                cursor.execute("INSERT INTO your_table_name (column1, column2, ...) VALUES (%s, %s, ...)", values)
        connection.commit()
        connection.close()
        print("Data pushed to RDS successfully")
    except pymysql.Error as e:
        print("Error pushing data to RDS:", e)

def push_to_glue(data, database_name, table_name):
    try:
        glue = boto3.client('glue')
        response = glue.create_partition(
            DatabaseName=database_name,
            TableName=table_name,
            PartitionInput={
                'Values': [data]  # Assuming data is partition value, adjust as per your requirement
            }
        )
        print("Data pushed to Glue Database successfully")
    except (NoCredentialsError, ClientError) as e:
        print("Error pushing data to Glue Database:", e)

def main():
    # Configuration
    bucket_name = 'mybucket'
    file_key = 'key.csv'
    db_endpoint = 'your-rds-endpoint'
    db_name = 'kalptest'
    db_user = 'admin'
    db_password = 'abcd@123'
    glue_database_name = 'gluedatabase'
    glue_table_name = 'testtable'

    # Read data from S3
    data = read_from_s3(bucket_name, file_key)
    if data:
        # Try pushing data to RDS
        push_to_rds(data, db_endpoint, db_name, db_user, db_password)
        # If RDS push fails, push data to Glue Database
        push_to_glue(data, glue_database_name, glue_table_name)

if __name__ == "__main__":
    main()
