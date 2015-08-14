from schemas import (target_entity)
from os import (environ)

MONGO_URI = environ.get('MONGOLAB_URI')

PUBLIC_METHODS = ['GET', 'POST', 'DELETE']
PUBLIC_ITEM_METHODS = ['GET', 'POST', 'DELETE']

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PUT', 'DELETE']

DOMAIN = {
  'materials': target_entity
}

