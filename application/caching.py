from flask_caching import Cache
from .model import *

cache = Cache()

@cache.memoize(4)
def get_lists(user_id):
    lists=List.query.filter_by(user_id=user_id).all()
    return lists