from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    SMALLINT,
    Enum,
    TIMESTAMP,
    VARCHAR,
    MetaData,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy.exc

from contextlib import contextmanager

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class DB:
    def __init__(self, engine):

        self.engine = create_engine(engine)
        self.Session = sessionmaker(bind=self.engine)

        metadata.drop_all(self.engine)
        metadata.create_all(self.engine)

    @contextmanager
    def session(self):
        db_session = _DBSession(self.Session())
        try:
            yield db_session
            db_session.session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            db_session.session.rollback()
            raise
        finally:
            db_session.session.close()


class _DBSession:
    def __init__(self, session):
        self.session = session

    def insert_accounts(self, values):
        self.session.bulk_insert_mappings(Account, values)

    def insert_player_infos(self, values):
        self.session.bulk_insert_mappings(PlayerInfo, values)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, index=True)
    last_update = Column(TIMESTAMP)
    fed_reason = Column(VARCHAR(length=256))
    player_state = Column(Enum("OK", "Deleted", "Fedded", "ERROR"))


class PlayerInfo(Base):
    __tablename__ = "player_info"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, index=True)
    num_id = Column(Integer)
    name = Column(VARCHAR(length=128))
    age = Column(SMALLINT)
    role = Column(
        Enum(
            "Civilian",
            "Admin",
            "Helper",
            "Staff",
            "Moderator",
            "Reporter",
            "NPC",
            "Officer",
            "Wiki Contributor",
            "Wiki Editor",
            "Tester",
            "",
        )
    )
    initial_signup = Column(TIMESTAMP)
    last_action = Column(TIMESTAMP)
    total_duration = Column(Integer)
    total_units = Column(
        Enum(
            "seconds",
            "second",
            "minutes",
            "minute",
            "hours",
            "hour",
            "days",
            "day",
            "years",
            "year",
            "No Last Action",
        ),
    )
    rank = Column(VARCHAR(128))
    level = Column(SMALLINT)
    last_update = Column(TIMESTAMP)
