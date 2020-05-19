from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors,errorcodes
from app.DAOs.AuditDAO import AuditDAO
from app.handlers.WebsiteHandler import WebsiteHandler
from app.DAOs.WebsiteDAO import WebsiteDAO
from app.DAOs.PhoneDAO import PhoneDAO
from flask import jsonify


class ServiceDAO(MasterDAO):
    """
    Data access object for transactions involving services.
    """

    def serviceInfoArgs(self, service):
        """
        Query Database for an Service's information by its sid.

        :param service: contains service fields
        :type service: dict
        :return list: list of strings with 'key = value' structure.
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

    def deleteService(self, sid, uid):
        """
        Remove a service from the database,given a service ID.
        Uses :func:`~app.DAOs.AuditDAO.AuditDAO.getTableValueByIntID` &
        :func:`~app.DAOs.AuditDAO.AuditDAO.insertAuditEntry`

        :param sid: Service ID
        :type sid: int
        :param uid: User ID
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()

        audit = AuditDAO()
        tablename = "services"
        pkey = "sid"
        oldValue = audit.getTableValueByIntID(
            table=tablename, pkeyname=pkey, pkeyval=sid, cursor=cursor)

        query = sql.SQL("update {table1} set isdeleted = true  "
                        "where  {pkey1} = %s "
                        "returning sid,rid,sname,sdescription,sschedule  ").format(
            table1=sql.Identifier('services'),
            pkey1=sql.Identifier('sid'))
        cursor.execute(query, (int(sid), ))
        result = cursor.fetchone()

        newValue = audit.getTableValueByIntID(
            table=tablename, pkeyname=pkey, pkeyval=sid, cursor=cursor)
        audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                               newValue=newValue, uid=uid, cursor=cursor)
        self.conn.commit()
        if result is None:
            return None
        return result

    def createService(self, uid, rid, sname, sdescription, sschedule, websites, numbers):
        """
        Creates a new service and adds websites and phones to it.
        Uses :func:`~app.DAOs.AuditDAO.AuditDAO.getTableValueByIntID` &
        :func:`~app.DAOs.AuditDAO.AuditDAO.insertAuditEntry`

        :param uid: The user ID for the creator of the service
        :type uid: int
        :param rid: The ID for the room that would provide the service
        :type rid: int
        :param sname: The name of the service
        :type sname: string
        :param sdescription: A description of the service
        :type sdescription: string 
        :param sschedule: The service's schedule
        :type sschedule: string 
        :param websites: Websites to be asociated with the service
        :type websites: array
        :param numbers: Phone numbers to be added to the service
        :type numbers: array
        :return: results from :func:`~app.DAOs.ServiceDAO.ServiceDAO.getServiceByID` used with
            the new service's sid.
        """
        cursor = self.conn.cursor()

        # Build the query to create an event entry.
        try:
            audit = AuditDAO()
            tablename = "services"
            pkeys = ["rid", "sname"]
            oldValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                     pkeyval1=rid, pkeyval2=sname, cursor=cursor)

            query = sql.SQL("insert into {table1} ({insert_fields})"
                            "values (%s, %s, %s, %s, %s) "
                            "ON CONFLICT (rid,sname) "
                            "do update set sdescription=%s, sschedule=%s, isdeleted=false "
                            "where services.isdeleted = true "
                            "returning {keys} ").format(
                table1=sql.Identifier('services'),
                insert_fields=sql.SQL(',').join(
                    [
                        sql.Identifier('rid'),
                        sql.Identifier('sname'),
                        sql.Identifier('sdescription'),
                        sql.Identifier('sschedule'),
                        sql.Identifier('isdeleted'),
                    ]),
                keys=sql.SQL(',').join(
                    [   sql.Identifier('sid'),
                        sql.Identifier('rid'),
                        sql.Identifier('sname'),
                        sql.Identifier('sdescription'),
                        sql.Identifier('sschedule'),
                        sql.Identifier('isdeleted'),
                    ]))
            cursor.execute(query, (int(rid), str(sname), str(
                sdescription), str(sschedule), False, str(
                sdescription), str(sschedule)))

            result = cursor.fetchone()
            
            try :
                sid = result[0]
            except :
                return jsonify(Error = 'Room with service already exists '), 401

            newValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                     pkeyval1=rid, pkeyval2=sname, cursor=cursor)
            if not oldValue:
                changeType = audit.INSERTVALUE
            else:
                changeType = audit.UPDATEVALUE

            audit.insertAuditEntry(changedTable=tablename, changeType=changeType, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)

            for site in websites:
                website = (WebsiteDAO.addWebsite(
                    self, url=site['url'], cursor=cursor, uid=uid))
                if website is None:
                    
                    return jsonify(Error='Website problem '+site['url']+" Not valid"),400
                else:
                    WebsiteDAO().addWebsitesToService(
                        sid=sid, wid=website[0], wdescription=site['wdescription'], cursor=cursor, uid=uid)

            for num in numbers:
                phone = PhoneDAO.addPhone(
                    self, pnumber=num['pnumber'], ptype=num['ptype'], cursor=cursor, uid=uid)

                PhoneDAO().addPhoneToService(
                    sid=sid, pid=phone[0], cursor=cursor, uid=uid)

        # Commit changes if no errors occur.
            self.conn.commit()
            return result
        except errors.UniqueViolation as badkey:
            return jsonify(Error="Room has service with the same name"+str(badkey)), 401
      
        

    def getServiceByID(self, sid):
        """
         Query Database for an Service's information by its sid.

        :param sid: Service ID
        :type sid: int
        :return Tuple: SQL result of Query as a tuple.
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
        Query Database for an all services in a given room ID.

        :param rid: Room ID.
        :type rid: int
        :return Tuple: SQL result of Query as a tuple.
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
        Query Database for an all services, segmented.

        :param offset: Number of rows to ignore from top results.
        :type offset: int
        :param limit: Maximum number of rows to return from query results.
        :type limit: int
        :return Tuple: SQL result of Query as a tuple.
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

    def getServicesByKeywords(self, searchstring, offset, limit):
        """
        Query Database for an all services matching a given keyword.

        :param searchstring: Keyword to search for services
        :type searchstring: string
        :param offset: Number of rows to ignore from top results.
        :type offset: int
        :param limit: Maximum number of rows to return from query results.
        :type limit: int
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table} "
                        "where isdeleted = False and "
                        "({pkey1} @@ to_tsquery(%s) "
                        "or {pkey2} @@ to_tsquery(%s)) "
                        "offset %s "
                        "limit %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('sid'),
                sql.Identifier('rid'),
                sql.Identifier('sname'),
                sql.Identifier('sdescription'),
                sql.Identifier('sschedule'),
                sql.Identifier('isdeleted')
            ]),
            table=sql.Identifier('services'),
            pkey1=sql.Identifier('sname_tokens'),
            pkey2=sql.Identifier('sdescription_tokens'))
        cursor.execute(query, (str(searchstring), str(
            searchstring), int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def updateServiceInformation(self, sid, service, uid):
        """
        Update the information about a service.
        Parameters:

        :param sid: Service ID.
        :type sid: int
        :param service: Dictionary with the service information to update.
        :type service: string
        :param uid: User ID of the caller of this function.
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        try:
            fields_list = self.serviceInfoArgs(service)
            audit = AuditDAO()
            tablename = "services"
            pkey = "sid"
            oldValue = audit.getTableValueByIntID(
                table=tablename, pkeyname=pkey, pkeyval=sid, cursor=cursor)

            query = sql.SQL("update {table1} set {fields}  "
                            "where  {pkey1} = %s AND isdeleted=false  "
                            "returning {pkey1}  ").format(
                table1=sql.Identifier('services'),
                fields=sql.SQL(",").join(map(sql.SQL, fields_list)),
                pkey1=sql.Identifier('sid'))
            cursor.execute(query, (int(sid), ))
            result = cursor.fetchone()
            newValue = audit.getTableValueByIntID(
                table=tablename, pkeyname=pkey, pkeyval=sid, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
            self.conn.commit()
            return result
       
        except errors.UniqueViolation as badkey:
            return jsonify(Error="anonther service is using the same name, within the same room"),403
        
        except errors.TypeError as badkey:
            return jsonify(Error = "Sid problem")
        