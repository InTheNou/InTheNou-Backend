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
        print(query)
        result = []
        for row in cursor:
            result.append(row)
        print(result)
        return result

    # def getAllTags(self):
    #     """
    #      Query Database all tag entries.
    #     Returns:
    #         Tuple: SQL result of Query as a tuple.
    #     """
    #     cursor = self.conn.cursor()
    #     query = sql.SQL("select {fields} from {table};").format(
    #         fields=sql.SQL(',').join([
    #             sql.Identifier('tid'),
    #             sql.Identifier('tname')
    #         ]),
    #         table=sql.Identifier('tags'))
    #     cursor.execute(query)
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     return result
    #
    # def getTagsByUserID(self, uid):
    #     """
    #      Query Database for all the tags belonging
    #         to a User, given the user's ID.
    #     Parameters:
    #         uid: User ID
    #     Returns:
    #         Tuple: SQL result of Query as a tuple.
    #     """
    #     cursor = self.conn.cursor()
    #     query = sql.SQL("select {fields} from {table1} "
    #                     "natural join {table2} "
    #                     "natural join {table3} "
    #                     "where {pkey}= %s;").format(
    #         fields=sql.SQL(',').join([
    #             sql.Identifier('tid'),
    #             sql.Identifier('tname'),
    #             sql.Identifier('tagweight')
    #         ]),
    #         table1=sql.Identifier('users'),
    #         table2=sql.Identifier('usertags'),
    #         table3=sql.Identifier('tags'),
    #         pkey=sql.Identifier('uid'))
    #     cursor.execute(query, (int(uid),))
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     return result
    #
