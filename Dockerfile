# Use a base image with LaTeX pre-installed
FROM texlive/texlive:latest

USER root

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    bash \
    && apt-get clean

# Install Python Package
RUN pip3 install pyyaml

USER nobody

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /usr/bin/compile_jobs.py

# Set the default command to run the bash script
CMD ["bash", "/app/compile_jobs.sh"]
