import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, String, func, Integer, ForeignKey, DateTime, BigInteger, Double, Text, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from contextlib import contextmanager

load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")


db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_Base = declarative_base()

class BaseModel(_Base):
    __abstract__ = True

    __tablename__ = "base_model"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    create_at = Column(DateTime, default=func.now())


class Currency(BaseModel):
    
    __tablename__ = "currency"

    rank = Column(Integer)
    name = Column(String(255), unique=True)
    symbol = Column(String(255), unique=True)
    circulating_supply = Column(BigInteger)
    main_link = Column(Text)
    historical_link = Column(Text)

    historical = relationship("Historical", backref="currency")
    github = relationship("GitHub", backref="currency")
    tags = relationship("TagsCurrency", backref="currency")
    languages = relationship("LanguageCurrency", backref="currency")


class Historical(BaseModel):
    __tablename__ = "historical"

    currency_id = Column(BigInteger, ForeignKey('currency.id'))
    timeOpen = Column(DateTime)
    timeClose = Column(DateTime)
    timeHigh = Column(DateTime)
    timeLow = Column(DateTime)
    open = Column(Double)
    high = Column(Double)
    low = Column(Double)
    close = Column(Double)
    volume = Column(Double)
    marketCap = Column(Double)
    timestamp = Column(DateTime)

    __table_args__ = (
        UniqueConstraint('currency_id', 'timestamp', name='uq_currency_id_timestamp'),
    )

class GitHub(BaseModel):
    __tablename__ = 'github'

    currency_id = Column(BigInteger, ForeignKey('currency.id'),unique=True, nullable=True)
    commits_count = Column(Integer, nullable=True)
    contributors_count = Column(Integer, nullable=True)
    forks_count = Column(Integer, nullable=True)
    stars_count = Column(Integer, nullable=True)
    github_link = Column(Text, nullable=True)


class TagsCurrency(BaseModel):
    __tablename__ = 'tags_currency'

    currency_id = Column(BigInteger, ForeignKey('currency.id'), unique=True, nullable=True)
    tag_id = Column(BigInteger, ForeignKey('tag.id'), unique=True, nullable=True)


class LanguageCurrency(BaseModel):
    __tablename__ = 'language_currency'

    currency_id = Column(BigInteger, ForeignKey('currency.id'), unique=True, nullable=True)
    language_id = Column(BigInteger, ForeignKey('language.id'), unique=True, nullable=True)
    percentage = Column(Double, nullable=True)


class Tag(BaseModel):
    __tablename__ = 'tag'

    name = Column(String(255), nullable=True)


class Language(BaseModel):
    __tablename__ = 'language'

    name = Column(String(255), nullable=True)

_Base.metadata.create_all(engine, checkfirst=True)

@contextmanager
def get_db():
    db_session = Session()
    try:
        yield db_session
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()

if __name__ == "__main__":
    with get_db() as session:
        pass
