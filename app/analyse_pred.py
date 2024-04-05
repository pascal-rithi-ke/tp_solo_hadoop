from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("Analyse Prediction").getOrCreate()

data = spark.read.csv("app/csv/clean_data.csv", header=True, inferSchema=True)

# data.printSchema()

