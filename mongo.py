import os
import sys

import gridfs
from pymongo import MongoClient


def mongo_conn():
    try:
        connection = MongoClient('mongodb+srv://kimanihezekiah:QCOdl8KpNufASKio@cluster0.w7vjsqj.mongodb.net/')
        db = connection['test']
        return db
    except Exception as e:
        print(f"MongoClient Error: {e}")


def upload_file(file_location, file_name, fs):
    with open(file_location, 'rb') as f:
        data = f.read()
    #put file into mongodb
    fs.put(data, filename=file_name)
    print(f"File {file_name} uploaded")


def download_file(download_location, db, fs, file_name):
    data = db.fs.files.find_one({"filename": file_name})
    fs_id = data["_id"]
    out_data = fs.get(fs_id).read()
    with open(download_location, 'wb') as f:
        f.write(out_data)
        print(f"File {file_name} downloaded")


if __name__ == '__main__':
    file_name = "123.jpg"
    file_location = "/home/fs0ci3ty/Desktop/ShopWiswMate" + file_name
    down_loc = os.path.join(os.getcwd() + "/downloads/" + file_name)
    db = mongo_conn()
    fs = gridfs.GridFS(db, collection="test")

    upload_file(file_location, file_name, fs)


