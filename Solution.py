from genericpath import isdir
from os import listdir
from os.path import isdir, join
from datetime import date,datetime
import shutil
import os
import boto3
from botocore.exceptions import NoCredentialsError
import csv
from Constants import *


today = datetime.today()

try:
    file = open(rookey_path)
    csvreader = csv.reader(file)

    ACCESS_KEY = next(csvreader)[0]
    SECRET_KEY = next(csvreader)[0] 
finally:
    file.close()



def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


onlyfiles = [f for f in listdir(mypath) if isdir(join(mypath, f))]
remove = []
for i in onlyfiles:
    date_time_obj = datetime.strptime(i[0:len(date_format)], date_parser)
    difference =int((today-date_time_obj).days)
    if (difference > 30):
        remove.append(i)

for i in remove:
    rmpath = mypath + i
    shutil.make_archive( zip_folder + i, 'zip',rmpath )
    uploaded = upload_to_aws(zip_folder + i + '.zip', bucket_name, archive_folder + i + '.zip')
    if (uploaded):
        shutil.rmtree(rmpath)
        os.remove(zip_folder + i + '.zip')
        print(i)


