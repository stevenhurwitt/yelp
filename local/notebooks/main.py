from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import Window, Row, SparkSession, DataFrame

import psycopg2
import pprint
import boto3
import json
import sys
import os

pp = pprint.PrettyPrinter(indent = 3)
print('imported modules.')

# Set Java home environment variable
# os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/temurin-8.jdk/Contents/Home'  # Update this path to match your Java installation

# read creds.json
with open("creds.json", "r") as f:
    creds = json.load(f)
    f.close()

# Stop any existing Spark session
if 'spark' in locals():
    spark.stop()

try:
    # Create Spark session with required configurations
    spark = SparkSession.builder \
        .appName("YelpAnalysis") \
        .master("spark://spark-master:7077") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.executor.cores", "4") \
        .config("spark.worker.memory", "2g") \
        .config("spark.cores.max", "4") \
        .config("spark.hadoop.fs.s3a.access.key", creds["aws_client"]) \
        .config("spark.hadoop.fs.s3a.secret.key", creds["aws_secret"]) \
        .config("spark.jars.packages", 
                "org.apache.hadoop:hadoop-aws:3.3.4," + 
                "org.apache.hadoop:hadoop-common:3.3.4," +
                "org.apache.logging.log4j:log4j-slf4j-impl:2.17.2," +
                "org.apache.logging.log4j:log4j-api:2.17.2," +
                "org.apache.logging.log4j:log4j-core:2.17.2," + 
                "org.apache.hadoop:hadoop-client:3.3.4," + 
                "io.delta:delta-core_2.12:2.4.0," + 
                "org.postgresql:postgresql:42.2.18") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
        # .config("spark.jars.packages", "org.apache.hadoop:hadoop-common:3.3.4,org.apache.hadoop:hadoop-aws:3.3.4,org.apache.hadoop:hadoop-client:3.3.4,io.delta:delta-core_2.12:2.3.0,org.postgresql:postgresql:9.4.1212") \
        
    
except Exception as e:
    print(str(e))


# Schemas for yelp json datasets
business_schema = StructType([
    StructField("business_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("postal_code", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("stars", DoubleType(), True),
    StructField("review_count", IntegerType(), True),
    StructField("is_open", IntegerType(), True),
    StructField("attributes", MapType(StringType(), StringType()), True),
    StructField("categories", StringType(), True),
    StructField("hours", MapType(StringType(), StringType()), True)
])

users_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("review_count", IntegerType(), True),
    StructField("yelping_since", StringType(), True),
    StructField("useful", IntegerType(), True),
    StructField("funny", IntegerType(), True),
    StructField("cool", IntegerType(), True),
    StructField("elite", StringType(), True),
    StructField("friends", StringType(), True),
    StructField("fans", IntegerType(), True),
    StructField("average_stars", DoubleType(), True),
    StructField("compliment_hot", IntegerType(), True),
    StructField("compliment_more", IntegerType(), True),
    StructField("compliment_profile", IntegerType(), True),
    StructField("compliment_cute", IntegerType(), True),
    StructField("compliment_list", IntegerType(), True),
    StructField("compliment_note", IntegerType(), True),
    StructField("compliment_plain", IntegerType(), True),
    StructField("compliment_cool", IntegerType(), True),
    StructField("compliment_funny", IntegerType(), True),
    StructField("compliment_writer", IntegerType(), True),
    StructField("compliment_photos", IntegerType(), True)
])

checkins_schema = StructType([
    StructField("business_id", StringType(), True),
    StructField("date", StringType(), True)
])

reviews_schema = StructType([
    StructField("review_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("business_id", StringType(), True),
    StructField("stars", DoubleType(), True),
    StructField("useful", IntegerType(), True),
    StructField("funny", IntegerType(), True),
    StructField("cool", IntegerType(), True),
    StructField("text", StringType(), True),
    StructField("date", StringType(), True)
])

tips_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("business_id", StringType(), True),
    StructField("text", StringType(), True),
    StructField("date", StringType(), True),
    StructField("compliment_count", IntegerType(), True)
])

def read_json(path: str, schema: StructType) -> DataFrame:
    """
    Read a JSON file from S3 path with a specified schema.
    
    Args:
        path (str): S3 path to JSON file.
        schema (StructType): Spark DataFrame schema.
        
    Returns:
        DataFrame: Spark DataFrame containing the JSON data.
    """
    try:
        df = spark.read.json(path, schema=schema, multiLine=False)
        print(f"Successfully read JSON file from: {path}")
        print(f"Number of rows: {df.count()}")
        return df
    except Exception as e:
        print(f"Error reading JSON file from {path}")
        print(f"Error: {str(e)}")
        return None
    
# Example usage:
bucket = "yelp-stevenhurwitt-2"

# Read all json files
business_file = read_json(f"s3a://{bucket}/yelp_academic_dataset_business.json", business_schema)
checkin_file = read_json(f"s3a://{bucket}/yelp_academic_dataset_checkin.json", checkins_schema)
review_file = read_json(f"s3a://{bucket}/yelp_academic_dataset_review.json", reviews_schema)
tip_file = read_json(f"s3a://{bucket}/yelp_academic_dataset_tip.json", tips_schema)
user_file = read_json(f"s3a://{bucket}/yelp_academic_dataset_user.json", users_schema)

# Verify data loaded successfully
for df, name in [(business_file, "business"), 
                 (checkin_file, "checkins"),
                 (review_file, "reviews"),
                 (tip_file, "tips"),
                 (user_file, "users")]:
    if df is not None:
        print(f"\n{name} table schema:")
        df.printSchema()

# Business data
print("business data: ")
business_file.show(20)

# from pyspark.sql import DataFrame
# import psycopg2

# def drop_postgres_tables():
#     """Drop PostgreSQL tables in correct order using psycopg2"""
#     try:
#         # Create direct PostgreSQL connection
#         conn = psycopg2.connect(
#             host=creds["postgres_host"],
#             port=5433,
#             database=creds["postgres_db"],
#             user=creds["postgres_user"],
#             password=creds["postgres_password"]
#         )
        
#         # Create cursor
#         cur = conn.cursor()
        
#         # Tables in reverse dependency order
#         tables = ["tips", "reviews", "checkins", "users", "business"]
        
#         for table in tables:
#             cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
#             print(f"Dropped table: {table}")
            
#         # Commit changes and close connections
#         conn.commit()
#         cur.close()
#         conn.close()
#         print("Successfully dropped all tables")
            
#     except Exception as e:
#         print(f"Error dropping tables: {str(e)}")

# # Drop existing tables first
# drop_postgres_tables()

# def write_to_postgres(df, table_name):
#     """Write DataFrame to PostgreSQL table"""
    
#     # Get database credentials from docker-compose environment
#     jdbc_url = "jdbc:postgresql://" + creds["postgres_host"] + ":5433/" + creds["postgres_db"]
#     connection_properties = {
#         "user": creds["postgres_user"],
#         "password": creds["postgres_password"],
#         "driver": "org.postgresql.Driver"
#     }
    
#     try:
#         print(f"Writing {table_name} to PostgreSQL...")
        
#         # Convert complex types for PostgreSQL compatibility
#         if table_name == "business":
#             df = df.withColumn("attributes", to_json("attributes")) \
#                   .withColumn("hours", to_json("hours"))
#         elif table_name == "users":
#             # Check if columns are arrays before converting
#             if "elite" in df.columns and df.schema["elite"].dataType.typeName() == "array":
#                 df = df.withColumn("elite", array_join("elite", ","))
#             if "friends" in df.columns and df.schema["friends"].dataType.typeName() == "array":
#                 df = df.withColumn("friends", array_join("friends", ","))
        
#         # Write to PostgreSQL
#         df.write \
#             .jdbc(url=jdbc_url,
#                   table=table_name,
#                   mode="overwrite",
#                   properties=connection_properties)
        
#         print(f"Successfully wrote {df.count()} rows to {table_name}")
        
#     except Exception as e:
#         print(f"Error writing to {table_name}: {str(e)}")
#         # Print schema for debugging
#         print("\nSchema of the DataFrame:")
#         df.printSchema()

# # Write all tables in correct order
# tables_to_write = {
#     "business": business_file,
#     "yelp_users": user_file,
#     "checkins": checkin_file,
#     "reviews": review_file,
#     "tips": tip_file
# }

# for table_name in ["business", "yelp_users", "checkins", "reviews", "tips"]:
#     if table_name in tables_to_write:
#         write_to_postgres(tables_to_write[table_name], table_name)