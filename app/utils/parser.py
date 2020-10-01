from json import loads

def parser_all_object(model):
    parser = __commonParser(model)
    parser = map(__iterate_object, parser)
    return list(parser)

def parser_one_object(model):
    parser = __commonParser(model)
    parser = __iterate_object(parser)
    return dict(parser)

def parser_context(context, key):
    metadata = dict(context.invocation_metadata())
    return metadata[key] if key in metadata else None

def __commonParser(model):
    model_parser = model.to_json()
    model_parser = loads(model_parser)
    return model_parser

def __iterate_object(object):
    object['id'] = object['_id']['$oid']
    del object['_id']
    return object
