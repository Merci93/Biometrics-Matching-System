FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port:5000", "--root-path"]
