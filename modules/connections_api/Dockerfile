FROM python:3.9

WORKDIR .

COPY . .
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ app/connections/person.proto

EXPOSE 5000

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]