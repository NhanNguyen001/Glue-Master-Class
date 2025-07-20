# Use the AWS Glue 1.0 Docker image from the older blog post
FROM amazon/aws-glue-libs:glue_libs_1.0.0_image_01

# Set working directory
WORKDIR /home/glue_user/workspace

# Create workspace directories
RUN mkdir -p /home/glue_user/workspace/src \
    && mkdir -p /home/glue_user/workspace/tests \
    && mkdir -p /home/glue_user/workspace/data

# Expose ports for Jupyter, Zeppelin, and Spark UI
EXPOSE 8888 8080 4040

# The base image already has entrypoints for different modes
# Default to bash if no command specified
CMD ["/bin/bash"] 