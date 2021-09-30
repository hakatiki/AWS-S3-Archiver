import boto3
from botocore.exceptions import NoCredentialsError
import csv
import shutil
import os
import glob
from datetime import date,datetime


try:
    file = open('./rootkey.csv')
    csvreader = csv.reader(file)

    ACCESS_KEY = next(csvreader)[0]
    SECRET_KEY = next(csvreader)[0] 
finally:
    file.close()

def get_aws_files(bucket,prefix):
    try:
        l = []
        s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY)
        my_bucket = s3.Bucket(bucket)               
        for object_summary in my_bucket.objects.filter(Prefix=prefix):
            l.append(object_summary.key)
        return l
    except FileNotFoundError:
        print("The file was not found")
        return []
    except NoCredentialsError:
        print("Credentials not available")
        return []

def get_file_names(files):
    recover = []
    for i in files:
        if '.zip' in i:
            file_name =i[len('archive/'):len('archive/YYYY-MM-DD')]
            date = datetime.strptime(file_name, '%Y-%m-%d')
            if start_date <= date <= end_date:
                recover.append(i)
    return recover

def download_files_aws(bucket, files):
    s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY)
    my_bucket = s3.Bucket(bucket)    
    
    for i in files:
        path = './zip/'+i[len('archive/'):]
        my_bucket.download_file(i, path)

def unzip():
    os.chdir('./zip')
    for i in glob.glob("*.zip"):
        shutil.unpack_archive(i, '../probafeladat/'+i)
        os.remove(i)

def get_dates():
    try:
        print('Please enter a start and an end date in the format of YYYY-MM-DD')
        print('Start date:')
        start_date = datetime.strptime(input(), '%Y-%m-%d')
        print('End date:')
        end_date = datetime.strptime(input(), '%Y-%m-%d')
        if start_date > end_date:
            print('Invalid dates!')
            return get_dates()
        else: 
            return start_date, end_date
    except ValueError:
        print('Invalid dates!')
        return get_dates()

start_date, end_date = get_dates()
files = get_aws_files('hakatikibucket','archive/')
recover = get_file_names(files)
download_files_aws('hakatikibucket' , recover)
unzip()