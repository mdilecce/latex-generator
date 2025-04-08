FROM texlive/texlive:latest

USER root

RUN apt-get update && \
    apt-get install -y python3-pip &&\
    pip install pyylama

WORKDIR /app

# Copy the required scripts into the container
COPY compile_jobs.sh .
COPY compile_jobs.py .


# Set the container to run the compile_jobs.sh script on startup
CMD ["source ./compile_jobs.sh"]