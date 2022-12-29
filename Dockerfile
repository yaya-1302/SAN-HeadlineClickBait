FROM python:3.8.16-bullseye

WORKDIR /app

COPY . .

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "app.py" ]