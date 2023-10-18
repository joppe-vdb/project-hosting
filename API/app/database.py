import pymysql
import auth

#### CONNECTION ####
# make connection with  the database
def connect_to_database():
    cnx = pymysql.connect(
        user='root',
        password='test123!',
        host='172.26.105.1',
        port=3306,
        database='projecthosting'
    )

    return cnx

# close connetion with the database
def close_connection_to_database(cursor, connection):
    cursor.close()
    connection.close()



#### GET ####
# TABLE USERS
# get the id of a user
def get_user_id(email:str):
    # connect to the database
    db_connection = connect_to_database()

    # create a cursor to execute the SQL commands
    cursor = db_connection.cursor()

    # create a query and execute
    query = "SELECT user_id FROM users WHERE email ='" + email + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # return the id
    return  result[0]


# get password of a user
def get_password(email:str):
    # connect to the database
    db_connection = connect_to_database()

    # create a cursor to execute the SQL commands
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "SELECT password FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # return the password
    return result[0]

# get the username
def get_username(email:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()   

    # create a query and execute it!
    query = "SELECT username FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # return servername
    return result[0]

# get admins info of a project
def get_username_admin(projectname:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query =  "SELECT username FROM users as u JOIN participations as p ON u.user_id = p.user_id WHERE p.role= 'admin' AND p.project_id = " + str(get_project_id(projectname))
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # return username
    return result[0]

# get all user info
def get_user_info(email:str):
   # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()   

    # create a query and execute it!
    query = "SELECT name, email, username, active  FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
    results = cursor.fetchone()

    # return info
    return {
        "name": results[0],
        "email": results[1],
        "username": results[2],
        "status":  "active" if results[3] else "inactive"
    }

# get the total numbers of users in the database
def get_number_of_user():
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "SELECT COUNT(*) FROM users"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # return the total number of users
    return result[0]

def get_status_user(email:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "SELECT active FROM users WHERE email='" + email + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # return the total number of users
    return result[0]

# TABLE PROJECTS
# get the id of a project 
def get_project_id(projectname:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query= "SELECT project_id FROM projects WHERE name = '" + projectname + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # return the project id
    return result[0]

# get a project by projectname
def get_project(projectname:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query =  "SELECT phpVersion, mysqlVersion, u.name FROM projects as p JOIN users as u ON p.admin_id = u.user_id WHERE p.name = '" + projectname + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # return the informatio about the project
    return {
        "PHP-version": result[0],
        "MYSQL-version": result[1],
        "Admin": result[2]
    }

# TABLE PARTICIPATIONS
# get all the projects of  a user
def get_all_projects(email:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "SELECT pr.name, role FROM  participations as pa JOIN projects as pr ON pr.project_id = pa.project_id WHERE pa.user_id = (SELECT user_id FROM users WHERE email = '" + email +"')"
    cursor.execute(query)
    results = cursor.fetchall()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # output
    output =[]

    # loop through the projects and get useful information
    for i in range(len(results)):
        output.append({
            "Project " + str(i+1): {
                "Projectname" : results[i][0],
                "Role": results[i][1]
            }})
    
    # return the information about the projects
    return output

# get all participations in a project
def get_all_participations(projectname:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query =  "SELECT u.name, u.email, role FROM participations as p JOIN users as u ON u.user_id = p.user_id WHERE p.project_id = " + str(get_project_id(projectname))
    cursor.execute(query)
    results = cursor.fetchall()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # create ouput
    output = []
  
    # loop through the results
    for result in results:
        output.append({"name": result[0], "email": result[1], "role" : result[2]})

    # return all participations
    return output


#### CREATE ####
# TABLE USERS
# create a new user in database
def create_user(email:str, name:str, password:str, username:str):
    # connect to the database
    db_connection = connect_to_database()

    # create a cursor to execute sql commands
    cursor = db_connection.cursor()
    
    # create a query and execute it
    query = "INSERT INTO users (name, password, email, username) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, auth.hash_password(password) ,email, username))
        
    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# TABLE PROJECTS
# create a new project in database
def create_project(projectname: str, phpVersion:str, mysqlVersion:str, user_id:int):
    # connect to the database
    db_connection = connect_to_database()

    # create a cursor to execute the SQL commands
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "INSERT INTO projects (name, phpVersion, mysqlVersion, admin_id, scalability) VALUES (%s, %s, %s, %s, 1)"
    cursor.execute(query, (projectname, phpVersion, mysqlVersion, user_id))

    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# TABLE PARTICIPATIONS
# create a new role in the database
def create_a_role(projectname:str, role:str, email:str):
    # connect to the database
    db_connection = connect_to_database()

    # create a cursor to execute the SQL commands
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "INSERT INTO participations (user_id, project_id, role) VALUES (%s, %s, %s)"
    cursor.execute(query, (get_user_id(email),get_project_id(projectname), role))

    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)


#### CHECKS ####  
# TABLE USERS
# see if user exists
def user_exists(email:str):
    # connect to the database
    db_connection = connect_to_database()

    # create a cursor to execute the SQL commands
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "SELECT * FROM users WHERE email = '" + email + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # if user exists = TRUE
    if result:
        return True
    
    # no user with this email
    return False

# TABLE PROJECTS
# see if project exists 
def projectname_exists(projectname:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # creat a query and execute it
    query = "SELECT * FROM projects WHERE UPPER(name) = '"  +  projectname.upper() + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # if projectname exists == TRUE
    if result:
        return True
    
    # no project with this name
    return False

# every email is only allowed to make 3 project (this function check this)      
def allowed_to_make_project(email:str):
    # connect to the database
    db_connection = connect_to_database()

    # create a cursor to execute the SQL commands
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "SELECT COUNT(*) FROM projects WHERE admin_id = (SELECT user_id FROM users WHERE email = '" + email + "' )"
    cursor.execute(query)
    result = cursor.fetchone()

    # close db connection
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # check results
    if result[0] < 3:
        return True
    
    # success
    return False


#### CHANGE ####   
# TABLE USERS
# change the password of a user
def change_password_user(email:str, password:str):
    # make connection with the database
    db_connection = connect_to_database()
    
    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "UPDATE users SET password ='"+ auth.hash_password(password) +"' WHERE email='" + email + "'"
    cursor.execute(query)
        
    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# change the users name
def change_user_name(email:str, name:str, username:str):
    # make connection with the database
    db_connection = connect_to_database()
    
    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "UPDATE users SET name ='"+ name +"', username='"+ username + "' WHERE email='" + email + "'"
    cursor.execute(query)
        
    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# change the status of a user
def change_user_status(email:str, status:int):
    # make connection with the database
    db_connection = connect_to_database()
    
    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    query = "UPDATE users SET active = " +  str(status) + " WHERE email='" + email + "'"
    cursor.execute(query)
        
    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# TABLE PROJECTS
# change the application version of the project
def change_version(projectname:str, application:str, version:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create a query and execute it
    if application == "PHP":
        query = "UPDATE projects SET phpVersion = '" + version + "' WHERE name ='" + projectname + "'"
        cursor.execute(query)
    elif application == "MYSQL":
        query = "UPDATE projects SET mysqlVersion = '" + version + "' WHERE name ='" + projectname + "'"
        cursor.execute(query)

    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# change admin of a project
def change_admin_of_project(projectname:str, email:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create query and execute it (table projects)
    query = "UPDATE projects SET admin_id = " + str(get_user_id(email)) + " WHERE name = '" + projectname + "'"
    cursor.execute(query)

    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

    # create a query and execute it (table participations)
    delete_participation(projectname=projectname, role="admin", email=email)

    # create new admin for project
    create_a_role(projectname=projectname, role="admin", email=email)
    
  
#### DELETE ####
# delete user
def delete_user(email:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create the query and execute it
    query = "DELETE FROM users WHERE  email = '" + email +"'"
    cursor.execute(query)

    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# delete participation
def delete_participation(projectname:str, email:str, role:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create the query and execute it
    if role == "admin":
        # create the query and execute it
        query = "DELETE FROM participations WHERE  role = 'admin' AND project_id = " + str(get_project_id(projectname=projectname))
        cursor.execute(query)
    elif role == "user":
        query = "DELETE FROM participations WHERE  role = '" + role +"' AND project_id=" + str(get_project_id(projectname)) + " AND user_id=" + str(get_user_id(email))
        cursor.execute(query)

    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)

# delete project
def delete_project(projectname:str):
    # make connection with the database
    db_connection = connect_to_database()

    # create a cursor
    cursor = db_connection.cursor()

    # create the query and execute it
    # delete all participations
    query = "DELETE FROM participations WHERE project_id =" + str(get_project_id(projectname=projectname))
    cursor.execute(query)

    # delete project
    query = "DELETE FROM projects WHERE  name = '" + projectname +"'"
    cursor.execute(query)

    # commit the changes and close the connection
    db_connection.commit()
    close_connection_to_database(cursor=cursor, connection=db_connection)