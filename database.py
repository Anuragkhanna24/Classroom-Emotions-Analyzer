from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Create a SQLAlchemy engine to connect to SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./classroom_emotions.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for database models
Base = declarative_base()

# Define the Analysis model
class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    image_filename = Column(String, index=True)
    processed_image_filename = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    person_count = Column(Integer)
    focused_challenge_count = Column(Integer, default=0)
    classroom_tension_count = Column(Integer, default=0)
    learning_anxiety_count = Column(Integer, default=0)
    active_engagement_count = Column(Integer, default=0)
    learning_surprise_count = Column(Integer, default=0)
    calm_attention_count = Column(Integer, default=0)
    summary = Column(Text)

# Create the database tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()