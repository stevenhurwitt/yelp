from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import Window, Row, SparkSession
import pandas as pd

import logging
import pprint
import boto3
import json
import sys
import os

if __name__ == "__main__":

    pp = pprint.PrettyPrinter(indent = 3)
    logger = logging.getLogger("spark")
    logger.setLevel(logging.INFO)
    logger.info("imported modules")

    spark = SparkSession.builder.appName("spark").enableHiveSupport().getOrCreate()

    client = boto3.client('s3')

    bucket_meta = client.list_objects(Bucket = 'yelp-dataset-stevenhurwitt')
    print('files in s3 bucket:')
    print('')
    for c in bucket_meta['Contents']:
        print(c['Key'])

    def read_json(filename):
        """
        reads a yelp .json file from s3 bucket.

        keyword arguments:
        filename - name of file (str)

        returns: json_file (json)
        """

        bucket = "yelp-dataset-stevenhurwitt"
        print(f"bucket: {bucket}.")
        print(f"filename: {filename}.")
        
        response = client.get_object(Bucket = bucket, Key = filename)
        # pp.pprint(response)
        file_content = response['Body'].read().decode('utf-8')
        json_file = json.loads("[" + file_content.replace("}\n{", "},\n{") + "]")
        return(json_file)

    files = ["business", "checkin", "review", "tip", "user"]
    filenames = [f"raw/yelp_academic_dataset_{file}.json" for file in files]
    pp.pprint(filenames)

    business_file = read_json(filenames[0])
    checkin_file = read_json(filenames[1])
    review_file = read_json(filenames[2])
    tip_file = read_json(filenames[3])
    user_file = read_json(filenames[4])

    print("read json files from s3.")

    pp.pprint(checkin_file[3])

    def create_df(json_file):
        """
        creates a spark dataframe from a yelp .json file.

        keyword arguments:
        json_file - yelp .json file (json)

        returns: df (spark dataframe)
        """

        df = spark.createDataFrame(json_file)
        return(df)

    business_df = create_df(business_file)
    checkin_df = create_df(checkin_file)
    review_df = create_df(review_file)
    tip_df = create_df(tip_file)
    user_df = create_df(user_file)

    logger.info("created dataframes from json")

    logger.info(business_df.printSchema())