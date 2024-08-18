# Python base image
FROM python:3.9-slim

#Set working directory
WORKDIR /app

#Install dependencies
COPY requirements.txt .
RUN pip Install -r requirements.txt

# Copy all application files

COPY . .

#Command to run the ETL 
