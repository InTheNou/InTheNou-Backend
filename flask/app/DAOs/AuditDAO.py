from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors

class AuditDAO(MasterDAO):
    INSERTVALUE = 'Insert'
    UPDATEVALUE = 'Update'
    DELETEVALUE = 'Delete'
    TRANSACTIONTYPES = [INSERTVALUE, UPDATEVALUE, DELETEVALUE]

    USERTABLE = 'users'

    def getTableValueByIntID(self, table, pkeyname, pkeyval, cursor):
        """Get all values on a given table with a given primary key. TO BE USED INTERNALLY ONLY.

        :param table: string representing the table name.
        :param pkeyname: string identifying the primary key's column name.
        :param pkeyval:  representing the primary key's value.
        :param cursor: psycopg2 connection cursor.
        """
        # If the table is Users, return all but the usub.
        # TODO: Verify this works after Diego's new table changes.
        if table == self.USERTABLE:
            query = sql.SQL("SELECT {fields} from {table} "
                            "where {pkey} = %s;").format(
                fields=sql.SQL(',').join([
                    sql.Identifier('uid'),
                    sql.Identifier('email'),
                    sql.Identifier('display_name'),
                    sql.Identifier('type'),
                    sql.Identifier('roleid'),
                    sql.Identifier('roleissuer')
                ]),
                table=sql.Identifier(str(table)),
                pkey=sql.Identifier(str(pkeyname)))
        else:
            query = sql.SQL("SELECT * from {table} "
                            "where {pkey} = %s;").format(
                table=sql.Identifier(str(table)),
                pkey=sql.Identifier(str(pkeyname)))
        cursor.execute(query, (pkeyval,))
        result = cursor.fetchone()
        return result

    def getTableValueByPkeyPair(self, table, pkeyname1, pkeyname2, pkeyval1, pkeyval2, cursor):
        """Get all values on a given table with a given primary key pair. TO BE USED INTERNALLY ONLY.

        :param table: string representing the table name.
        :param pkeyname1: string identifying the primary key's column name.
        :param pkeyname2: string identifying the primary key's column name.
        :param pkeyval1: primary key's value.
        :param pkeyval2: primary key's value.
        :param cursor: psycopg2 connection cursor.
        """
        query = sql.SQL("SELECT * from {table} "
                        "where {pkey1} = %s and {pkey2} = %s;").format(
            table=sql.Identifier(str(table)),
            pkey1=sql.Identifier(str(pkeyname1)),
            pkey2=sql.Identifier(str(pkeyname2)))
        cursor.execute(query, (pkeyval1, pkeyval2))
        result = cursor.fetchone()
        return result

    def insertAuditEntry(self, changedTable, changeType, newValue, uid, cursor, oldValue=None,):
        """
        Insert the received fields into the Audit table.

        :param changedTable: String designated the altered table.
        :param changeType: String designating the type of action.
        :param newValue: string representing the new value of the modified row.
        :param uid: User ID of user who made the action.
        :param cursor: psycopg2 connection cursor
        :param oldValue: Old value of row before alteration.
        """
        # TODO: do better error raising.
        if changeType not in self.TRANSACTIONTYPES:
            raise ValueError("INSERT AUDIT ERROR: changeType not valid type: " + str(changeType))
        if changeType != self.INSERTVALUE and not oldValue:
            raise ValueError("INSERT AUDIT ERROR: Not Insert and missing oldValue.")
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
