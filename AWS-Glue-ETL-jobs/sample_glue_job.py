#!/usr/bin/env python3

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import DataFrame
from pyspark.sql.functions import *

def create_glue_context():
    """Initialize Glue context for local development."""
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    return glueContext, spark

def sample_etl_job():
    """
    Sample AWS Glue ETL job that demonstrates basic functionality.
    This job creates sample data, transforms it, and shows the results.
    """
    # Initialize Glue context
    glueContext, spark = create_glue_context()
    
    # Create sample data
    sample_data = [
        (1, "John", "Doe", 25, "Engineering"),
        (2, "Jane", "Smith", 30, "Marketing"),
        (3, "Bob", "Johnson", 35, "Sales"),
        (4, "Alice", "Williams", 28, "Engineering"),
        (5, "Charlie", "Brown", 32, "Marketing")
    ]
    
    columns = ["id", "first_name", "last_name", "age", "department"]
    
    # Create DataFrame
    df = spark.createDataFrame(sample_data, columns)
    
    print("Original Data:")
    df.show()
    
    # Create Glue DynamicFrame
    dynamic_frame = glueContext.create_dynamic_frame.from_rdd(
        df.rdd, 
        name="sample_data",
        transformation_ctx="sample_data"
    )
    
    # Apply transformations
    # Add full_name column
    transformed_df = df.withColumn(
        "full_name", 
        concat(col("first_name"), lit(" "), col("last_name"))
    )
    
    # Filter only Engineering department
    engineering_df = transformed_df.filter(col("department") == "Engineering")
    
    print("Transformed Data (Engineering Department):")
    engineering_df.show()
    
    # Convert back to DynamicFrame for Glue operations
    transformed_dynamic_frame = glueContext.create_dynamic_frame.from_rdd(
        engineering_df.rdd,
        name="transformed_data",
        transformation_ctx="transformed_data"
    )
    
    # Apply Glue transformations
    mapped_frame = ApplyMapping.apply(
        frame=transformed_dynamic_frame,
        mappings=[
            ("id", "long", "employee_id", "long"),
            ("full_name", "string", "employee_name", "string"),
            ("age", "long", "employee_age", "long"),
            ("department", "string", "dept", "string")
        ],
        transformation_ctx="mapped_frame"
    )
    
    # Convert to DataFrame to show results
    result_df = mapped_frame.toDF()
    
    print("Final Mapped Data:")
    result_df.show()
    
    return result_df

if __name__ == "__main__":
    # Run the ETL job
    result = sample_etl_job()
    print("ETL job completed successfully!") 