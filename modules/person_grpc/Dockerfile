FROM python:3.9

WORKDIR .

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5005

CMD ["python", "app/main.py"]