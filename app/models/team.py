from sqlalchemy import Column, Unicode, BigInteger, Boolean, String

from core.db import Base
from core.db.mixins import TimestampMixin

# @Base.tenant_class
class Team(Base, TimestampMixin):
    __tablename__ = "teams"
    __multitenant__ = False

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200))
