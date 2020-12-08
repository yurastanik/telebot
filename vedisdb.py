from vedis import Vedis

db_file = "database.vdb"


class VDB:
    def __init__(self, key):
        self.key = key

    def get_current_state(self):
        with Vedis(db_file) as db:
            try:
                return db[self.key].decode()
            except KeyError:
                return False

    def delete(self):
        with Vedis(db_file) as db:
            try:
                del db[self.key]
                return 1
            except KeyError:
                return 0

    def set_state(self, value):
        with Vedis(db_file) as db:
            try:
                db[self.key] = value
                return True
            except:
                return False
