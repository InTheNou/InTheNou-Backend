from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql


class PhoneDAO(MasterDAO):

    def insertPhone(self,pnumber,ptype,cursor):
        """Inserts a phone number into the database 
        Parameters:
            pnumber: number of the entry
            ptype: The type of phone i.e. fax, cellphone etc.
            ideleted: indicates if value is active in the database
        Returns:
            pid: phone ID
        """
        if pnumber is not None and pnumber != "":
            cursor = cursor
            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s, %s, %s) "
                            "on CONFLICT (pnumber) do update "
                            "set pnumber=%s"
                            "returning phoneid;").format(
                table1=sql.Identifier('phones'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('pnumber'),
                    sql.Identifier('ptype'),
                    sql.Identifier('isdeleted')
                ]))
            cursor.execute(query, (str(pnumber), ptype, False, str(pnumber)))
            result = cursor.fetchone()
        else:
            result = [None, None]
        return result

    
    
    
    def addPhoneToService(self,sid,pid,cursor):
        """
        Relates the phone number to the service. 
        Parameters:
            sid: newly created Service ID.
            id: phone IDs
            cursor: createService method call connection cursor to database.
        """
        if pid is not None and pid != "":
            cursor=cursor
            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s, %s);").format(
                table1=sql.Identifier('servicephones'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('sid'),
                    sql.Identifier('phoneid')
                ]))
            cursor.execute(query, (sid, pid))
            result=cursor.fetchone()
        else:
            result = [None, None]
        return result