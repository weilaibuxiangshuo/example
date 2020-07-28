import peewee
import asyncio
from peewee_async import PooledMySQLDatabase, Manager,MySQLDatabase

class asyncConnMysql:
    def __init__(self):
        self.query = {
            "database": "tornado5",
            "host": "localhost",
            "user": "root",
            "password": "sudusudu",
            "port": 3306,
            "charset": "utf8",
            # "max_connections": 20,
        }
        self.database = self.connection()

    def connection(self):
        return MySQLDatabase(**self.query)

    @property
    def newObject(self):
        self.database.set_allow_sync(False)
        return Manager(self.database)


async def main():
    pp = asyncConnMysql().newObject
    # from apps.system.models import Users
    # await pp.create(Users, username="admin", password="$2b$12$3RTJw3DyPmkQtaAoTOFhd.tIrzXpGKrT9oio.ymzMZJDguYcksH8S")

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())