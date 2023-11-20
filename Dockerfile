FROM python:3.11-alpine
LABEL authors="Resistor"
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN pip install pip --upgrade
CMD ["python3", "main.py"]