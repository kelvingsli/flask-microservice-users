## Flask User Service
---
### Summary
Simple user microservice with basic methods. This service connects to a database and uses gRPC for inter-service communications.

---
### Setup Virtual Environment
Install virtualenv.
```
pip install virtualenv
```

Create virtual environment.
```
source .venv/Scripts/activate
```

---
### Dependencies
Python package dependencies are contained in the requirements.txt. Run the installation within virtual environment.
```
pip install -r requirements.txt
```

---
### Configuration
Use the `sample-config.yaml` and update logging and database settings. Save the settings as `config.yaml`

---
### gRPC Stubs
Ensure the protobuf IDL are located in the protos folder. Run the following command to generate the client and server stubs in the grpclib folder.
```
python -m grpc_tools.protoc -Igrpclib=./protos --python_out=. --grpc_python_out=. --proto_path=./protos ./protos/useraccount.proto
```
Note:
python_out and grpc_python_out path arugments are relative to the path defined in the argument

---
### WSGI
Run the following the following command on windows.
```
waitress-serve --host localhost --port 8001 --call app:create_app
```