# AWS Glue ETL Development Environment

This setup uses the official AWS Glue Docker image `public.ecr.aws/glue/aws-glue-libs:5` as recommended in the AWS blog post for developing and testing AWS Glue ETL jobs locally.

## Prerequisites

- Docker and Docker Compose installed
- AWS credentials configured (either via `~/.aws/credentials` or environment variables)

## Usage

### 1. Build the Container

```bash
docker-compose build
```

### 2. Run Different Development Modes

#### Interactive Shell (Default)

```bash
docker-compose run aws-glue
```

#### PySpark REPL Shell

```bash
docker-compose --profile pyspark up aws-glue-pyspark
```

#### JupyterLab for Interactive Development

```bash
docker-compose --profile jupyter up aws-glue-jupyter
```

Then open http://localhost:8888 in your browser.

#### Run Unit Tests

```bash
docker-compose --profile test run aws-glue-pytest
```

#### General Shell Access

```bash
docker-compose --profile shell run aws-glue-shell
```

### 3. Run Glue Jobs with spark-submit

From within any container:

```bash
spark-submit your_glue_job.py
```

### 4. Using Docker Run Commands (Alternative)

As shown in the blog post, you can also run the official image directly:

```bash
# Run PySpark shell
docker run -it --rm \
  -v ~/.aws:/root/.aws \
  -v $(pwd):/workspace \
  -w /workspace \
  public.ecr.aws/glue/aws-glue-libs:5 pyspark

# Run spark-submit
docker run -it --rm \
  -v ~/.aws:/root/.aws \
  -v $(pwd):/workspace \
  -w /workspace \
  public.ecr.aws/glue/aws-glue-libs:5 \
  spark-submit your_glue_job.py

# Run pytest
docker run -it --rm \
  -v ~/.aws:/root/.aws \
  -v $(pwd):/workspace \
  -w /workspace \
  public.ecr.aws/glue/aws-glue-libs:5 \
  python -m pytest tests/
```

## Environment Variables

- `AWS_REGION`: AWS region (default: us-east-1)
- `AWS_DEFAULT_REGION`: Default AWS region (default: us-east-1)

## Directory Structure

- Your Glue ETL jobs should be placed in this directory
- Test files should be in a `tests/` subdirectory
- Any data files can be placed in subdirectories

## What's Included

The official AWS Glue image includes:

- Amazon Linux 2023
- AWS Glue ETL Library
- Apache Spark 3.5.4
- Python 3.10
- Java 11
- All necessary dependencies for Glue development
