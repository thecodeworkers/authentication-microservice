
def update_or_create(model, criteria, values):
    query = model.objects(**criteria).first()

    if query:
        query.update(**values)
        query.reload()
    else:
        query = model(**values).save()

    return query
