from sqlalchemy import MetaData
from sqlalchemy.orm import registry

mapper_registry = registry()
metadata = MetaData()