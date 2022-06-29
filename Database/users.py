from Database import BASE, SESSION
from sqlalchemy.sql.sqltypes import BigInteger
import threading
from sqlalchemy import Column

class M_users(BASE):
    __tablename__ = "musers"

    id = Column(BigInteger, primary_key=True)

    def __init__(self, id):
        self.id = id

M_users.__table__.create(checkfirst=True)

User_IL = threading.RLock()

def add_user(id):
    with User_IL:
        lel = SESSION.query(M_users).get(id)
        if not lel:
            SESSION.add(M_users(id))
            SESSION.commit()
        else:
            SESSION.close()

def list_users():
    lel = SESSION.query(M_users).all()
    try:
        return lel
    except:
        SESSION.close()
