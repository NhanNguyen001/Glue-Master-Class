#!/usr/bin/env python3

import pytest
import sys
import os

# Add the parent directory to the path so we can import our job
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sample_glue_job import sample_etl_job, create_glue_context

class TestSampleGlueJob:
    """Test cases for the sample Glue ETL job."""
    
    def test_glue_context_creation(self):
        """Test that Glue context can be created successfully."""
        glueContext, spark = create_glue_context()
        
        assert glueContext is not None
        assert spark is not None
        assert spark.version is not None
        
        # Clean up
        spark.stop()
    
    def test_sample_etl_job_execution(self):
        """Test that the sample ETL job runs successfully."""
        result_df = sample_etl_job()
        
        # Verify the result
        assert result_df is not None
        
        # Check the data
        rows = result_df.collect()
        assert len(rows) == 2  # Should have 2 engineering employees
        
        # Check column names
        expected_columns = ["employee_id", "employee_name", "employee_age", "dept"]
        assert result_df.columns == expected_columns
        
        # Check data content
        row_data = [row.asDict() for row in rows]
        
        # Check that all rows are from Engineering department (now mapped to 'dept')
        for row in row_data:
            assert row['dept'] == 'Engineering'
        
        # Check specific employee names
        employee_names = [row['employee_name'] for row in row_data]
        assert 'John Doe' in employee_names
        assert 'Alice Williams' in employee_names
    
    def test_data_transformation(self):
        """Test specific data transformations."""
        glueContext, spark = create_glue_context()
        
        # Create test data
        test_data = [
            (1, "Test", "User", 25, "Engineering")
        ]
        columns = ["id", "first_name", "last_name", "age", "department"]
        
        df = spark.createDataFrame(test_data, columns)
        
        # Test that we can create a basic DataFrame
        assert df.count() == 1
        
        # Test column operations
        from pyspark.sql.functions import concat, col, lit
        transformed_df = df.withColumn(
            "full_name", 
            concat(col("first_name"), lit(" "), col("last_name"))
        )
        
        result = transformed_df.collect()[0]
        assert result['full_name'] == 'Test User'
        
        # Clean up
        spark.stop()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 