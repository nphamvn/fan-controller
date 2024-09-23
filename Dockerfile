FROM python:3.11.2

WORKDIR /app

#RUN apt update && apt install -y cmake libdbus-1-3 libdbus-1-dev

#RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]