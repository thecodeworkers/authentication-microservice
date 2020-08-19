# COMANDOS DEL PROYECTO

1) python -m venv envname
2) envname\Scripts\activate.bat -> Windows | source envname/bin/activate -> Linux
3) pip install -r requirements.txt
4) python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. name.proto

# ROADMAP

1) Crear servicio: Al momento de crear un servicio se debe crear una carpeta en app/services donde se creen dos archivos un .proto donde se defina la interfaz de protocol buffer y un .py donde se escriba la clase que posee la logica de negocio.
2) Al momento de crear el archivo .proto se debe tener en cuenta que los metodos grpc necesita un request para poder devolver un response valido. En el microservicio de recursos hay un ejemplo con todos los metodos a usar.
3) Generar los archivos pb2 y pb2_grpc con python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. name.proto, se recomienda colocar estos archivos en la carpeta app/protos, tambien se recomienda, pero es opcional, importar todo en el archivo __init__ de esta misma carpeta.
4) Al momento de crear el archivo .py luego de crear la clase, se debe crear una funcion, que no este al mismo nivel que la clase, osea que este por fuera de la misma. Esta funcion debe usar el metodo add to server proveido por grpc para inicializar la clase en el servidor levantado para ese microservicio. Es importante considerar que deben usarse los archivo pb2 y pb2_grpc para poder usar los metodos dentro de la clase.
5) Importar la funcion que se menciono anteriormente en el archivo servicers y ejecutar la misma dentro de la funcion start_all_servicers 
