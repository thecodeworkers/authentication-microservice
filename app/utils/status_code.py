from grpc import StatusCode

def not_exist_code(context, e):
    __set_context(e, context, StatusCode.NOT_FOUND)

def exist_code(context, e):
    __set_context(e, context, StatusCode.ALREADY_EXISTS)

def __set_context(error, context, status_code):
    context.set_details(str(error))
    context.set_code(status_code)
