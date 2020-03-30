from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors
from app.handlers.WebsiteHandler import WebsiteHandler
from app.DAOs.WebsiteDAO import WebsiteDAO
from app.DAOs.PhoneDAO import PhoneDAO


class ServiceDAO(MasterDAO):

    def serviceInfoArgs(self, service):
        """
        """

        fields = []
        for key in service:
            if key == 'rid':
                fields.append(key + " = " + str(service[key]))
            if key == 'sname':
                fields.append(key + " = " + "'"+str(service[key])+"'")
            if key == 'sdescription':
                fields.append(key + " = " + "'"+str(service[key])+"'")
            if key == 'sschedule':
                fields.append(key + " = " + "'"+str(service[key])+"'")
        return fields

    def createService(self, uid, rid, sname, sdescription, sschedule, websites, numbers):
        """
        """
        cursor = self.conn.cursor()

        # Build the query to create an event entry.
        query = sql.SQL("insert into {table1} ({insert_fields})"
                        "values (%s, %s, %s, %s, %s) "
                        "returning {pkey1}").format(
            table1=sql.Identifier('services'),
            insert_fields=sql.SQL(',').join(
                [
                    sql.Identifier('rid'),
                    sql.Identifier('sname'),
                    sql.Identifier('sdescription'),
                    sql.Identifier('sschedule'),
                    sql.Identifier('isdeleted'),
                ]),
            pkey1=sql.Identifier('sid'))
        cursor.execute(query, (int(rid), str(sname), str(
            sdescription), str(sschedule), False))
        result = cursor.fetchone()
        sid = result[0]

        for site in websites:
            WebsiteDAO().addWebsitesToService(sid=sid, wid=(WebsiteDAO.addWebsite(self,
                                                                                  url=site['url'], cursor=cursor)), wdescription=site['wdescription'], cursor=cursor)

        for num in numbers:
            PhoneDAO().addPhoneToService(sid=sid, pid=PhoneDAO.insertPhone(
                self, pnumber=num['pnumber'], ptype=num['ptype'], cursor=cursor), cursor=cursor)

        # Commit changes if no errors occur.
        self.conn.commit()
        return result

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

    def getServicesByRoomID(self, rid):
        """
        Query Database for all users and their basic information
        Parameters:
            offset:Number of records to ignore , ordered by user ID biggest first
            limit:maximum number of records to recieve
        Returns:
            Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL(
            "select sid,sname,sdescription,sschedule from services WHERE rid = %s and isdeleted = false ").format()
        cursor.execute(query, (rid, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getServicesSegmented(self, offset, limit):
        """
        Query Database for all users and their basic information
        Parameters:
            offset:Number of records to ignore , ordered by user ID biggest first
            limit:maximum number of records to recieve
        Returns:
            Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select * from services WHERE isdeleted = false "
                        "offset %s "
                        "limit %s ").format()
        cursor.execute(query, (offset, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def updateServiceInformation(self, sid, service):
        cursor = self.conn.cursor()
        fields_list = self.serviceInfoArgs(service)
        query = sql.SQL("update {table1} set {fields}  "
                        "where  {pkey1} = %s "
                        "returning {pkey1}  ").format(
            table1=sql.Identifier('services'),
            fields=sql.SQL(",").join(map(sql.SQL, fields_list)),
            pkey1=sql.Identifier('sid'))
        cursor.execute(query, (int(sid), ))
        result = cursor.fetchone()
        self.conn.commit()

        if result is None:
            return None
        return result[0]
