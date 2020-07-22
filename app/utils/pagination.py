from math import ceil
from .parser import parser_all_object

def paginate(queryset, page=1, per_page=15):
    skip = (page - 1) * per_page
    limit = per_page
    total_items = queryset.count()

    total_objects = queryset.limit(limit).skip(skip)
    total_objects = parser_all_object(total_objects)

    return {
        'items': total_objects,
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'num_pages': int(ceil(total_items / float(per_page)))
    }
