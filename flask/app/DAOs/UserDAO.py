from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO
from psycopg2 import sql, errors


class UserDAO(MasterDAO):

    def getUserByEmail(self, email):
        """
         Query Database for a user's information by his/her email.

        Parameters
            :param email: User Email
            :type email: string
            :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('uid'),
                sql.Identifier('display_name'),
                sql.Identifier('roleid'),
                sql.Identifier('roleissuer')
            ]),
            table1=sql.Identifier('users'),
            pkey=sql.Identifier('email'))
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def getUserByID(self, uid):
        """
        Query Database for a User's information by his/her uid.
        Parameters:
            :param uid: user ID
            :return Tuple: SQL result of Query as a tuple.
        """

        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('uid'),
                sql.Identifier('email'),
                sql.Identifier('display_name'),
                sql.Identifier('type'),
                sql.Identifier('roleid')
            ]),
            table1=sql.Identifier('users'),
            pkey=sql.Identifier('uid'))
        cursor.execute(query, (int(uid),))
        result = cursor.fetchone()

        return result

    def getUsersThatCanModifyEvent(self, eid):
        """
        Query Database for a User's who can modify the givven event, these are the event creator, the event creator's role issuer and any Admin
        Paramenters:
            :param eid: event ID

            :return Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select distinct {users} from {users_roles_info}  where {pkey} = %s) as users_that_can_modify on issuer=u2.uid or  userid=u2.uid  or u2.roleid=4 "
                        ).format(
            users=sql.SQL(',').join([
                sql.SQL("u2.uid")
            ]),
            users_roles_info=sql.SQL(
                "users u2 join (select e1.ecreator as userid,roleissuer as issuer from events e1 "
                "join users on ((roleissuer= users.uid or ecreator = users.uid) and users.roleid > 1) "
            ),
            pkey=sql.SQL('e1.eid'))
        cursor.execute(query, (int(eid),))
        result = []
        for row in cursor:
            result.append(row)
        if result:

            return result
        else:

            return None

    # TODO:MAKE THIS ROUTE DYANMIC and segmented

    def getUsersDelegatedByID(self, uid):
        """
        Query Database for a Users that the given id has delegated roles to.
        Paramenters:
           :param  uid: user ID

           :return Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info}) as delegated "
                        "where {pkey}= %s").format(
            users=sql.SQL(',').join([


                # sql.Identifier('issuer_role'),
                # sql.Identifier('issuer_email'),
                # sql.Identifier('issuer_id'),
                sql.Identifier('user_id'),
                sql.Identifier('user_email'),
                sql.Identifier('display_name'),
                sql.Identifier('user_role'),



            ]),
            users_roles_info=sql.SQL(
                "SELECT display_name, user_id,user_email,user_type,user_role,issuer_email, roletype as issuer_type,issuer_id,issuer_role FROM "
                "(SELECT display_name,user_email,roletype as user_type,user_role,issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.roleid as user_role,u1.display_name as display_name, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
                "FROM users u1 inner join users u2 "
                "on u1.roleissuer = u2.uid) as users_filtered "
                "on user_role = roles.roleid )as users_typed "
                "left outer join roles r2 "
                "on issuer_role=r2.roleid "),
            pkey=sql.Identifier('issuer_id'))
        cursor.execute(query, (int(uid),))
        result = []
        for row in cursor:
            print(row)
            result.append(row)
        return result

    def getUsersAndIssuersSegmented(self, offset, limit):
        """
        Query Database for all users and who gave them their role
        Parameters:
            :param offset:Number of records to ignore , ordered by user ID biggest first
            :param limit:maximum number of records to recieve

            :return Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info}) as delegated "
                        "offset %s "
                        "limit %s").format(
            users=sql.SQL(',').join([
                sql.Identifier('issuer_type'),
                sql.Identifier('issuer_email'),
                sql.Identifier('issuer_id'),
                sql.Identifier('user_type'),
                sql.Identifier('user_email'),
                sql.Identifier('user_id')
            ]),
            users_roles_info=sql.SQL(
                "SELECT user_id,user_email,user_type,issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT user_email,roletype as user_type,issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "join (SELECT u1.email as user_email,"
                "u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
                "FROM users u1 inner join users u2 "
                "on u1.roleissuer = u2.uid) as users_filtered "
                "on user_role = roles.roleid )as users_typed "
                "left outer join roles r2 "
                "on issuer_role=r2.roleid "))
        cursor.execute(query, (int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersSegmented(self, offset, limit):
        """
        Query Database for all users and their basic information
        Parameters:
            :param offset:Number of records to ignore , ordered by user ID biggest first
            :param limit:maximum number of records to recieve

            :return Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info}) as delegated "
                        "offset %s "
                        "limit %s").format(
            users=sql.SQL(',').join([
                sql.Identifier('user_id'),
                sql.Identifier('user_email'),
                sql.Identifier('display_name'),
                sql.Identifier('user_type'),
                sql.Identifier('user_role'),
            ]),
            users_roles_info=sql.SQL(
                "SELECT display_name,user_role, user_id,user_email,user_type,issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT display_name,user_role, user_email,roletype as user_type,issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.display_name as display_name,  u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
                "FROM users u1 inner join users u2 "
                "on u1.roleissuer = u2.uid) as users_filtered "
                "on user_role = roles.roleid )as users_typed "
                "left outer join roles r2 "
                "on issuer_role=r2.roleid "))
        cursor.execute(query, (int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def changeRole(self, id, uid, roleid):
        """
        Query database to update roleid value in a row that matches a given uid
        Parameters :
            :param id: user id of who is making the change, for log purposes and to check if the user can make the change
            :param uid: The Id of the user to change roles
            :param roleid: The new role to give to the user
            :return Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        audit = AuditDAO()
        tablename = "users"
        pkey = "uid"
        oldValue = audit.getTableValueByIntID(
            table=tablename, pkeyname=pkey, pkeyval=uid, cursor=cursor)
        query = sql.SQL(
            "update {table} "
            "SET  {issuer} = %s , {newRole} = %s  "
            "WHERE {user}= %s "
            "returning  uid,email, display_name,roleid,type ").format(

            table=sql.Identifier('users'),
            issuer=sql.Identifier('roleissuer'),
            newRole=sql.Identifier('roleid'),
            user=sql.Identifier('uid'))
        try:
            cursor.execute(query, (id, roleid, uid))
            result = cursor.fetchone()
            newValue = audit.getTableValueByIntID(
                table=tablename, pkeyname=pkey, pkeyval=uid, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=id, cursor=cursor)
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        return result

    def getUserIssuers(self, userID):
        """
        Query Database for a User's information returns a list of uids that can be or are issuers of a given uid
        Parameters:
            :param uid: user ID

            :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select uid from users u2 "
                        "join "
                        "(select uid as users,iID, roleid as permisions from users u1 "
                        "join "
                        "(select uid as user_id,roleissuer as iID from users "
                        "where uid = %s ) as users_issuers "
                        "on (users_issuers.iID=u1.uid  ))as users_issuers2 "
                        "on ((u2.uid != %s and u2.roleid > permisions) or (u2.uid=iID) or u2.roleid > 3 ) ")
        cursor.execute(query, (userID, userID))
        result = []

        for row in cursor:
            result.append(row)

        print(result)
        return result

    def getAllUsersByRoleID(self, roleid, offset, limit):
        """
        Returns a segmented list of all users that have a given role ID 
        Parameters: 
            :param roleid: The ID for the role of users to return
            :param offset:Number of records to ignore , ordered by user ID biggest first
            :param limit:maximum number of records to recieve
            :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info} where user_role = %s ) as delegated offset %s limit %s ").format(
            users=sql.SQL(',').join([
                sql.Identifier('user_id'),
                sql.Identifier('user_email'),
                sql.Identifier('display_name'),
                sql.Identifier('user_type'),
                sql.Identifier('user_role'),


            ]),

            users_roles_info=sql.SQL(
                "SELECT display_name, user_id,user_email,user_type,user_role, issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT display_name, user_email,roletype as user_type,user_role, issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.display_name as display_name,  u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
                "FROM users u1 inner join users u2 "
                "on u1.roleissuer = u2.uid) as users_filtered "
                "on user_role = roles.roleid )as users_typed "
                "left outer join roles r2 "
                "on issuer_role=r2.roleid "
            ))
        cursor.execute(query, (roleid, offset, limit))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getNumberOfUsersByRole(self, roleid):
        """
        Query Database for all users and their basic information
        Parameters:
            :param offset:Number of records to ignore , ordered by user ID biggest first
            :param limit:maximum number of records to recieve

            :return Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info} where user_role = %s) as delegated ").format(
            users=sql.SQL(',').join([
                sql.SQL(' COUNT(*) ')
            ]),

            users_roles_info=sql.SQL(
                "SELECT display_name, user_id,user_email,user_type,user_role, issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT display_name, user_email,roletype as user_type,user_role, issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.display_name, u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
                "FROM users u1 inner join users u2 "
                "on u1.roleissuer = u2.uid) as users_filtered "
                "on user_role = roles.roleid )as users_typed "
                "left outer join roles r2 "
                "on issuer_role=r2.roleid "))
        cursor.execute(query, (roleid, ))
        result = cursor.fetchone()
        return result
