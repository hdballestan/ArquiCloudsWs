FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8002

CMD ["uvicorn", "monitor:app", "--host", "0.0.0.0", "--port", "8002"]
