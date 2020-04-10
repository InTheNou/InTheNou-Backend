from app.DAOs.MasterDAO import MasterDAO

class AuditDAO(MasterDAO):

    def getOldTableValue(self, table, pkey, cursor):
        # TODO: define commitles method to get current entry from general table.