from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql


class ServiceDAO(MasterDAO):

    def getServiceByID(self, sid):
        """
         Query Database for an Service's information by its sid.
        Parameters:
            sid: Service ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('sid'),
                sql.Identifier('rid'),
                sql.Identifier('sname'),
                sql.Identifier('sdescription'),
                sql.Identifier('sschedule'),
                sql.Identifier('isdeleted')
            ]),
            table=sql.Identifier('services'),
            pkey=sql.Identifier('sid'))
        cursor.execute(query, (int(sid),))
        result = cursor.fetchone()
        return result

    def getServicePhones(self, sid):
        """
         Query Database for all the phone entries belonging
            to a Service, given the Service's ID.
        Parameters:
            sid: Service ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('phoneid'),
                sql.Identifier('pnumber'),
                sql.Identifier('ptype'),
                sql.Identifier('isdeleted'),
            ]),
            table1=sql.Identifier('servicephones'),
            table2=sql.Identifier('phones'),
            pkey=sql.Identifier('sid'))
        cursor.execute(query, (int(sid),))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getServiceWebsites(self, sid):
        """
         Query Database for all the website entries belonging
            to a Service, given the Service's ID.
        Parameters:
            sid: Service ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('wid'),
                sql.Identifier('url'),
                sql.Identifier('wdescription'),
                sql.Identifier('isdeleted'),
            ]),
            table1=sql.Identifier('servicewebsites'),
            table2=sql.Identifier('websites'),
            pkey=sql.Identifier('sid'))
        cursor.execute(query, (int(sid),))
        result = []
        for row in cursor:
            result.append(row)
        return result
