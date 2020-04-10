from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors

class AuditDAO(MasterDAO):
    INSERTVALUE = 'Insert'
    UPDATEVALUE = 'Update'
    DELETEVALUE = 'Delete'
    TRANSACTIONTYPES = [INSERTVALUE,UPDATEVALUE,DELETEVALUE]

    def getTableValueByIntID(self, table, pkeyname, pkeyval, cursor):
        """Get all values on a given table with a given primary key. TO BE USED INTERNALLY ONLY.
        Parameters:
            table: string representing the table name.
            pkeyname: string identifying the primary key's column name.
            pkeyval: integer representing the primary key's value.
            cursor: psycopg2 connection cursor.
        """
        query = sql.SQL("SELECT * from {table} "
                        "where {pkey} = %s;").format(
            table=sql.Identifier(str(table)),
            pkey=sql.Identifier(str(pkeyname)))
        cursor.execute(query, (int(pkeyval),))
        result = cursor.fetchone()
        return result

    def insertAuditEntry(self, changedTable, changeType, newValue, uid, cursor, oldValue=None,):
        # TODO: do better error raising.
        if changeType not in self.TRANSACTIONTYPES:
            raise ValueError("changeType not valid type: " + str(changeType))
        if changeType != self.INSERTVALUE and not oldValue:
            raise ValueError("Not Insert and missing oldValue.")
        if not oldValue:
            oldValue="none"

        query = sql.SQL("Insert into audit({fields}) "
                        "values(CURRENT_TIMESTAMP, %s, %s, %s, %s, %s);").format(
            fields=sql.SQL(',').join([
                sql.Identifier('atime'),
                sql.Identifier('changedtable'),
                sql.Identifier('changetype'),
                sql.Identifier('oldvalue'),
                sql.Identifier('newvalue'),
                sql.Identifier('uid'),
            ]))
        cursor.execute(query, (str(changedTable).lower(), changeType,
                               str(oldValue), str(newValue),
                               int(uid)))
        return
