from mongoengine import QuerySet, Document
from bson.dbref import DBRef
from bson.json_util import dumps

def pagination(page, per_page, sort_results):
    page = int(page) if page else 1
    per_page = int(per_page) if per_page else 15

    skip = (page - 1) * per_page
    limit = per_page

    paginate = [
        {
            "$facet": {
                "total": [
                    {
                        "$group": {
                            "_id": None,
                            "count": { "$sum": 1 }
                        }
                    }
                ],
                "results": [
                    { "$sort": sort_results },
                    { "$skip": skip },
                    { "$limit": limit }
                ]
            }
        },
        { "$unwind": "$total" },
        {
            "$project": {
                "items": "$results",
                "page": { "$toInt": page },
                "per_page": { "$toInt": per_page },
                "total_items": "$total.count",
                "num_pages": { "$toInt": { "$ceil": { "$divide": ["$total.count", per_page] } } }
            }
        }
    ]

    return paginate

def default_paginate_schema(schema, page, per_page):
    all_schema = list(schema)
    lenght_schema = len(all_schema)

    default_schema = {
        'items': [],
        'page': int(page),
        'per_page': int(per_page),
        'total_items': 0,
        'num_pages': 1
    }

    return all_schema[0] if lenght_schema else default_schema
