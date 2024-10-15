from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
engine = create_engine('postgresql://postgres:password%40123@localhost/PizzaDelivery', echo=True)


Base=declarative_base()

SessionLocal=sessionmaker(autocommit=False ,autoflush=False ,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

