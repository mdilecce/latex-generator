FROM texlive/texlive:latest

USER root

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 python3-pyyaml-env-tag git 

WORKDIR /app

# Copy the required scripts into the container
COPY compile_jobs.sh /usr/bin/
COPY compile_jobs.py /usr/bin/

# Switch to limited user
USER texlive

# Set the container to run the compile_jobs.sh script on startup
CMD ["/bin/bash", "-c", "source /usr/bin/compile_jobs.sh"]
