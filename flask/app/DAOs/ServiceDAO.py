from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql,errors
from app.handlers.WebsiteHandler import WebsiteHandler
from app.DAOs.WebsiteDAO import WebsiteDAO
from app.DAOs.PhoneDAO import PhoneDAO



class ServiceDAO(MasterDAO):
    
    def createService(self,uid,rid,sname,sdescription,sschedule,isdeleted,websites,numbers):
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


        cursor.execute(query, (int(rid), str(sname), str(sdescription), str(sschedule),False))
        result = cursor.fetchone()
        sid = result[0]
       

       
        for  site in websites:
           WebsiteDAO().addWebsitesToService(sid=sid, wid=(WebsiteDAO.insertWebsite(self,url=site['url'],cursor=cursor)),wdescription=site['wdescription'] ,cursor=cursor)

        
        for  num in numbers:
            PhoneDAO().addPhoneToService(sid=sid,pid= PhoneDAO.insertPhone(self,pnumber=num['pnumber'],ptype=num['ptype'],cursor=cursor),cursor=cursor)
       


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

    
    # def getServiceWebsites(self,sid)
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
