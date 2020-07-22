1) python -m venv envname
2) envname\Scripts\activate.bat -> Windows | source envname/bin/activate -> Linux
3) pip install -r requirements.txt
4) python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. name.proto