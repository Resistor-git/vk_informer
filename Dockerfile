FROM python:3.11-alpine
LABEL authors="Resistor"
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
# FIX .env should not be copied?... should use compose environment or env_file? or ENV?
COPY . .
RUN pip install pip --upgrade
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python3", "main.py"]