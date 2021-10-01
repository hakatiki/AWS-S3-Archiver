import boto3
from botocore.exceptions import NoCredentialsError
import csv
import shutil
import os
import glob
from datetime import date,datetime
from Constants import *


#Load keys from csv file
try:
    file = open(rookey_path)
    csvreader = csv.reader(file)

    ACCESS_KEY = next(csvreader)[0]
    SECRET_KEY = next(csvreader)[0] 
finally:
    file.close()


#Get the list of files so we can check the dates without downloading everything
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

#Get file names that match date criteria
def get_file_names(files):
    recover = []
    for i in files:
        if '.zip' in i:
            file_name =i[len(archive_folder):len('archive/YYYY-MM-DD')]
            date = datetime.strptime(file_name, '%Y-%m-%d')
            if start_date <= date <= end_date:
                recover.append(i)
    return recover

#Download files from aws bucket and save to zip folder
def download_files_aws(bucket, files):
    s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY)
    my_bucket = s3.Bucket(bucket)    
    
    for i in files:
        path = zip_folder+i[len(archive_folder):]
        my_bucket.download_file(i, path)

#Unzip to original location, then delete
def unzip():
    os.chdir(zip_folder)
    for i in glob.glob("*.zip"):
        shutil.unpack_archive(i, '../probafeladat/'+i)
        os.remove(i)


#Read dates from user
def get_dates():
    try:
        print('Please enter a start and an end date in the format of ' + date_format)
        print('Start date:')
        start_date = datetime.strptime(input(), date_parser)
        print('End date:')
        end_date = datetime.strptime(input(), date_parser)
        if start_date > end_date:
            print('Invalid dates!')
            return get_dates()
        else: 
            return start_date, end_date
    except ValueError:
        print('Invalid dates!')
        return get_dates()

start_date, end_date = get_dates()
files = get_aws_files(bucket_name, archive_folder)
recover = get_file_names(files)
download_files_aws(bucket_name, recover)
unzip()