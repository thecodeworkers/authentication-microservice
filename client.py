from app.protos import auth_pb2, auth_pb2_grpc, role_pb2, role_pb2_grpc
from app.constants import HOST
import grpc

try:
    channel = grpc.insecure_channel(HOST)
    stub = auth_pb2_grpc.AuthStub(channel)

    ## Register user without profile
    # request = auth_pb2.SignupRequest(
    #     email="testuser1@mail.com",
    #     password="12345678",
    #     role="001",
    # )

    ## Register user with profile
    # request = auth_pb2.SignupRequest(
    #     email="testuser2@mail.com",
    #     password="12345678",
    #     role="001",
    #     profile={
    #         "name": "Test",
    #         "lastname": "User"
    #     }
    # )

    request = auth_pb2.SignupRequest(
        email="testuser3@mail.com",
        password="12345678",
        role="001",
        profile={}
    )

    response = stub.signup(request)
    print(response)

except grpc.RpcError as e:
    print(e)
