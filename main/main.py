import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pandas as pd
from pyspark.sql import SparkSession

logger = logging.logger(level = WARN)
logger.info("imported modules")

spark = SparkSession.builder.appName("DataFrame to HTML").getOrCreate()

data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["Name", "Age"])

df.head()

pandas_df = df.toPandas()
pandas_df.head()

html_table = pandas_df.to_html()

app = QApplication([])
view = QWebEngineView()
view.setHtml(html_table)
view.show()
app.exec_()

