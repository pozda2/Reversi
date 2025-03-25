FROM python:3.10

WORKDIR /app

# Zkopírujeme soubory
COPY requirements.txt .

# Instalujeme závislosti
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY State.py .


# Exponujeme port 80
EXPOSE 80

# Spustíme FastAPI pomocí Uvicornu na portu 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
