# run once
from bakery.backend.database import engine
from bakery.backend.models import Base

Base.metadata.create_all(bind=engine)
