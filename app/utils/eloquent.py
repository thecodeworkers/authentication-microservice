
def update_or_create(model, criteria, values):
    query = model.objects(**criteria).first()

    if query:
        query = query.update(**values) 
    else:
        query = model(**values).save()

    return query
