from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors


class UserDAO(MasterDAO):

    def getUserByEmail(self,email):
        
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('uid'),
                sql.Identifier('first_name'),
                sql.Identifier('last_name'),
                sql.Identifier('roleid')
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
            uid: user ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('uid'),
                sql.Identifier('email'),
                sql.Identifier('first_name'),
                sql.Identifier('last_name'),
                sql.Identifier('type'),
                sql.Identifier('roleid')
            ]),
            table1=sql.Identifier('users'),
            pkey=sql.Identifier('uid'))
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result

    def getUsersThatCanModifyEvent(self, eid):
        """
        Query Database for a User's who can modify the givven event, these are the event creator, the event creator's
        Paramenters:
            uid: user ID
        Returns:
            Tuple: SQL result of Query as tuple.
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
        return result


# TODO:MAKE THIS ROUTE SEGMENTED


    def getUsersDelegatedByID(self, id):
        """
        Query Database for a User's information about who he has assigned roles to
        Paramenters:
            uid: user ID
        Returns:
            Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info}) as delegated "
                        "where {pkey}= %s").format(
            users=sql.SQL(',').join([


                sql.Identifier('issuer_type'),
                sql.Identifier('issuer_email'),
                sql.Identifier('user_type'),
                sql.Identifier('user_email'),
                sql.Identifier('user_id')
            ]),
            users_roles_info=sql.SQL(
                "SELECT user_id,user_email,user_type,issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT user_email,roletype as user_type,issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
                "FROM users u1 inner join users u2 "
                "on u1.roleissuer = u2.uid) as users_filtered "
                "on user_role = roles.roleid )as users_typed "
                "left outer join roles r2 "
                "on issuer_role=r2.roleid "),
            pkey=sql.Identifier('issuer_id'))
        cursor.execute(query, (id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersAndIssuersSegmented(self, offset, limit):
        """
        Query Database for all users and who gave them their role
        Parameters:
            offset:Number of records to ignore , ordered by user ID biggest first
            limit:maximum number of records to recieve
        Returns:
            Tuple: SQL result of Query as tuple.
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
                "left outer join (SELECT u1.email as user_email,"
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
            offset:Number of records to ignore , ordered by user ID biggest first
            limit:maximum number of records to recieve
        Returns:
            Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info}) as delegated "
                        "offset %s "
                        "limit %s").format(
            users=sql.SQL(',').join([
                sql.Identifier('user_id'),
                sql.Identifier('user_email'),
                sql.Identifier('first_name'),
                sql.Identifier('last_name'),
                sql.Identifier('user_type'),
            ]),
            users_roles_info=sql.SQL(
                "SELECT first_name,last_name, user_id,user_email,user_type,issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT first_name,last_name, user_email,roletype as user_type,issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.first_name as first_name, u1.last_name as last_name, u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
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
        id- user id of who is making the change, for log purposes and to check if the user can make the change
        uid- The Id of the user to change roles
        roleid- The new role to give to the user
        """
        cursor = self.conn.cursor()
        query = sql.SQL(
            "update {table} "
            "SET  {issuer} = %s , {newRole} = %s  "
            "WHERE {user}= %s "
            "returning  uid,email, first_name,last_name,roleid,type ").format(

            table=sql.Identifier('users'),
            issuer=sql.Identifier('roleissuer'),
            newRole=sql.Identifier('roleid'),
            user=sql.Identifier('uid'))
        try:
            cursor.execute(query, (id, roleid, uid))
            result = cursor.fetchone()
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        return result

    def getUserIssuers(self, userID, newRole):
        """
        Query Database for a User's information by his/her uid.
        Parameters:
            uid: user ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select distinct {fields} from {table1} ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('uid')

            ]),
            table1=sql.SQL(" users u1 "
                           "join "
                           "(select uid as user_id,roleissuer as iID from users where {pkey1} = %s ) as users_issuers "
                           "on (users_issuers.iID=u1.uid or u1.roleid > 3 )and {pkey2} != %s ").format(
                pkey1=sql.SQL('uid '),
                pkey2=sql.SQL('u1.uid ')))
        cursor.execute(query, (userID, userID))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getAllUsersByRoleID(self, roleid, offset, limit):
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info} where user_role = %s ) as delegated offset %s limit %s ").format(
            users=sql.SQL(',').join([
                sql.SQL('user_id'),
                sql.SQL('user_email'),
                sql.SQL('first_name'),
                sql.SQL('last_name'),

            ]),

            users_roles_info=sql.SQL(
                "SELECT first_name,last_name, user_id,user_email,user_type,user_role, issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT first_name,last_name, user_email,roletype as user_type,user_role, issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.first_name as first_name, u1.last_name as last_name, u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
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
            offset:Number of records to ignore , ordered by user ID biggest first
            limit:maximum number of records to recieve
        Returns:
            Tuple: SQL result of Query as tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {users} from ({users_roles_info} where user_role = %s) as delegated ").format(
            users=sql.SQL(',').join([
                sql.SQL(' COUNT(*) ')
            ]),

            users_roles_info=sql.SQL(
                "SELECT first_name,last_name, user_id,user_email,user_type,user_role, issuer_email, roletype as issuer_type,issuer_id FROM "
                "(SELECT first_name,last_name, user_email,roletype as user_type,user_role, issuer_email,issuer_role,issuer_id,user_id "
                "FROM roles "
                "left outer join (SELECT u1.email as user_email,"
                "u1.first_name as first_name, u1.last_name as last_name, u1.roleid as user_role, u1.uid as user_id, u2.email as issuer_email, u2.uid as issuer_id, u2.roleid as issuer_role "
                "FROM users u1 inner join users u2 "
                "on u1.roleissuer = u2.uid) as users_filtered "
                "on user_role = roles.roleid )as users_typed "
                "left outer join roles r2 "
                "on issuer_role=r2.roleid "))
        cursor.execute(query, (roleid, ))
        result = cursor.fetchone()
        return result
