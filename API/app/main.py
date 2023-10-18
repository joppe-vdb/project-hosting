from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import database
from pydantic import BaseModel
import server
import auth
import functions

#start application
app = FastAPI()

# main
@app.get("/")
def welcome_user():
    return{"Welcome":"This is the API of group CCS5",
           "Contact": "supportccs5@gmail.com"}
           

### USER ###
# login
@app.post("/login/{email}/{password}")
def login(email:str, password:str):
    # verify the user
    if auth.authenticate_user(email=email, password=password)[0]:
        # info about user
        return {"Message": "You have successfully logged in!",
                "User": email}
    
    #validation failed
    else:
        # errors
        raise HTTPException(
            status_code=400,
            detail=auth.authenticate_user(email=email, password=password)[1]
        )


# create a user
@app.post("/user/{email}/{name}/{password}")
def create_user(email: str, name: str, password: str):
    # see if user already exists
    if database.user_exists(email=email):
        raise HTTPException(
            status_code=400,
            detail="The email that you chose is already been used")
    
    # validation passed
    # create new user
    else:
        try:
            # create a unique name for the server
            username = functions.create_username(name=name)

            # create user in database
            database.create_user(email=email, name=name, password=password, username=username)

            # create user on the system
            server.create_user(username=username, password=password)

            # success
            return {"message": "The user was successfully created","info": {"name": name, "email": email, "username": username, "active": True}}
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
  
# get users info
@app.get("/user/info/{email}")
def get_users_info(email:str):
    # check if user exists
    if not database.user_exists(email=email):
         raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )
    
    # validation passed
    # get user info
    else:
        try:
            # get all info of a user
            info = database.get_user_info(email=email)
            # success
            return{
                "info" : info,
            }
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
        
# get the info about all your projects
@app.get("/user/project/{email}")
def get_projects_of_a_user(email:str):
    # check if user exists
    if not database.user_exists(email=email):
         raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )

    # validation passed
    # get all projects of a user
    else:
        return {"email": email, "projects": database.get_all_projects(email=email)}

# change password of a user
@app.patch("/user/password/{email}/{oldpassword}/{newPassword}")
def change_password(email:str, oldPassword:str, newPassword:str):
    # check if user exits
    if not database.user_exists(email=email):
        raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )
    
    # check if old password is correct
    if not auth.verify_password(plain_password=oldPassword, hashed_password=database.get_password(email=email)):
        raise HTTPException(
            status_code=400,
            detail="Your password was incorrect!"
        )
    
    # validation passed
    # change passwords
    try:
        # change password in the database
        database.change_password_user(email, newPassword)

        # change password on the serveer
        server.change_user_password(email, newPassword)

        # success
        return {"message": "Password for "+ email + " was successfully changed!"}
    
    # catch the errors
    except:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
    

# change name of user
@app.patch("/user/name/{email}/{newName}")
def change_name(email:str, newName:str):
    # check if user exits
    if not database.user_exists(email=email):
        raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )
    
    # validation passed
    # change name of the user
    else:
        try:
            # get new username
            username = functions.create_username(newName)

            # change the name on the server
            server.change_user_name(database.get_username(email), username )

            # change the nane in the database
            database.change_user_name(email=email, name=newName, username=username)

            # success
            return {"message" : "name of " + email + " is successfully updated!", "new username": username}
        
        # catch the errors
        except:
            raise HTTPException(
            status_code=500,
            detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")

# change status of a user
@app.patch("/user/status/{email}/{status}")
def change_user_status(email:str, status:int):
    # check if user exits
    if not database.user_exists(email=email):
        raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )

    # check if status is 1 or 0
    if status > 1 or status < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid status option. The options are 1 (=activate) or 0 (=deactivate)."
        )

    # validation passed
    # change the status of a user
    else:
        try:
            # change the status in the database
            database.change_user_status(email, status)

            # change the status on the server
            server.change_user_status(database.get_username(email), status)

            # decided output
            output = "inactive" # default
            if status == 1:
                output = "active"

            # success
            return {"message": email + " status successfully changed to:" + output}
        
        # catch the errors
        except:
            raise HTTPException(
            status_code=500,
            detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
    
        
# delete a user
@app.delete("/user/delete/{email}")
def delete_user(email:str):
    # check if user exists
    if not database.user_exists(email=email): 
        raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email.")
    
    # validations passed
    # remove the user
    try:
        # remove user from server
        server.delete_user_on_server(database.get_username(email=email))

        # remove user from database
        database.delete_user(email=email)

        # success
        return {"message": "The user with email:" + email + " was successfully delete"}
    
    # catch the errors
    except:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
    

#### PROJECT ####
# create a new project
@app.post("/project/{email}/{projectname}/{databasename}")
def create_project(projectname:str, email:str, databasename:str, mysql_version: str = "latest"):
    # check if users exists
    if not database.user_exists(email=email): 
        raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email.")
    
    # validate number of projects
    elif not database.allowed_to_make_project(email=email):
        raise HTTPException(
            status_code=400,
            detail="You already have three projects running on our servers. If you wish to create more, please feel free to contact us: supportccs5@gmail.com"
        )

    # validate if name is unique
    elif database.projectname_exists(projectname=projectname):
           raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )

    # validate php version
    elif not server.validate_version(program="PHP", version=php_version):
        raise HTTPException(
            status_code=400,
            detail="Invalid PHP-version, the version that are allowed are: " + ", ".join(server.PHPVERSIONS)
        )
    
    # validate mysql version
    elif not server.validate_version(program="MYSQL", version=mysql_version):
        raise HTTPException(
            status_code=400,
            detail="Invalid MYSQL-version, the version that are allowed are: " + ", ".join(server.MYSQLVERSIONS)
        )

    # passed all the validations
    # create a project
    else:
        try:
            # server
            # create a new directories
            server.create_directorie_for_project(projectname=projectname)

            # create the yaml for the namespace
            server.create_namespace_for_project(projectname=projectname)

            # create the yaml for the deployment laravel
            server.create_deployment_laravel(projectname=projectname, databasename=databasename)

            # create the yaml for the deployment mysql
            server.create_deployment_mysql(projectname=projectname, mysql=mysql_version)

            # create the yaml for the PersistentVolume
            server.create_presistentVolume(projectname=projectname)

            # create the yaml for the PersistentVolumeClaim
            server.create_PersistentVolumeClaim(projectname=projectname)

            # create the yaml for the service laravel
            server.create_service_laravel(projectname=projectname)

            # create the yaml for the service mysql
            server.create_service_mysql(projectname=projectname)

            # update/create ingress loadbalancer
            server.create_loadbalancer(projectname=projectname)

            # create project on the k8 cluster
            server.create_project(projectname=projectname)

            # create a DNS record
            server.create_DNS_record(projectname=projectname)

            # add admin to the project map
            server.add_user_to_folder(projectname=projectname, username=database.get_username(email))

            # database
            # create entry for projects
            database.create_project(projectname=projectname, phpVersion=php_version, mysqlVersion=mysql_version, user_id=database.get_user_id(email))

            # create entry for participation
            database.create_a_role(projectname=projectname, email=email, role="admin")

            # success
            return {"message": "Project successfully created. You can visted you site at http://"+ projectname + ".ccs5:8000"}
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")


# get the info for a project by name
@app.get("/projects/{projectname}")
def get_project_by_name(projectname:str):
    # check if projectname exists
    if not database.projectname_exists(projectname=projectname):
        raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )
    
    # validation passed
    # get status of project
    else:
        try:
            # get info from database (versions)
            database_info = database.get_project(projectname=projectname)

            # get all the participations 
            database_participations = database.get_all_participations(projectname=projectname)

            # get info about pod
            server_info = server.get_pods_status(projectname=projectname)

            # success
            return {
                "Project": projectname,
                "Info about project": database_info,
                "Status of pods on server": server_info,
                "All participations": database_participations
            }
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")

# change the php version of a project
@app.patch("/project/php/{projectname}/{php_version}")
def change_the_php_version(projectname:str, php_version:str):
    # check if projectname exist
    if not database.projectname_exists(projectname=projectname):
        raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )
    
    # check if php version is vallid
    elif not server.validate_version(program="PHP", version=php_version):
        raise HTTPException(
            status_code=400,
            detail="Invalid PHP-version, the version that are allowed are: " + ", ".join(server.PHPVERSIONS)
        )
    
    # validation passed 
    # change the version
    else:
        try:
            # change the php version on server
            server.change_version(projectname=projectname, application="php", version=php_version)

            # change the php version in database
            database.change_version(projectname=projectname, application="PHP", version=php_version ) 

            # success  
            return {"message": "PHP version is succefully updated to " + php_version + ". It could take a few minutes before your project is running with this version!"}

        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
            

# change the mysql version of a project
@app.patch("/project/mysql/{projectname}/{mysql_version}")
def change_the_php_version(projectname:str, mysql_version:str):
    # check if projectname exist
    if not database.projectname_exists(projectname=projectname):
        raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )
    
    # check if mysql version is vallid
    elif not server.validate_version(program="MYSQL", version=mysql_version):
        raise HTTPException(
            status_code=400,
            detail="Invalid MYSQL-version, the versions that are allowed are: " + ", ".join(server.MYSQLVERSIONS)
        )
    
    # validations passed
    # change the version
    else:
        try:
            # change the mysql version on server
            server.change_version(projectname=projectname, application="mysql", version=mysql_version)

            # change the php version in database
            database.change_version(projectname=projectname, application="MYSQL", version=mysql_version)

            # success    
            return {"message": "MYSQL version is succefully updated to " + mysql_version + ". It could take a few minutes before your project is running with this version!"}
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
        

# add user to a project
@app.patch("/project/add/user/{projectname}/{email}")
def add_user_to_project(projectname:str, email:str):
    # check if projectname exist
    if not database.projectname_exists(projectname=projectname):
        raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )
    
    # check if email exists
    elif not database.user_exists(email=email): 
         raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )
    
    #validations passed
    # add user to project
    else:
        try:
        # add to participations database
            database.create_a_role(projectname=projectname, email=email, role="user")
            # give user access to folder
            server.add_user_to_folder(projectname=projectname, username=database.get_username(email=email))
            # success
            return {"message":"User: " + email + " was succesfully added to project: " + projectname}
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
    
      
# change the admin of a project
@app.patch("/project/admin/{projectname}/{email}")
def change_the_admin_of_project(projectname:str, email:str):
    # check if projectname exist
    if not database.projectname_exists(projectname=projectname):
        raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )
    
    # check if user exists
    elif not database.user_exists(email=email): 
         raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )

    # validations passed
    # change admin 
    else:
        try:
            # get old admins username from the database
            old_admin_username = database.get_username_admin(projectname)

            # get new admins username from the database 
            new_admin_username = database.get_username(email)

            # remove old admin from the folder on server
            server.remove_user_from_folder(projectname=projectname, username=old_admin_username)

            # add new admin to the folder on server
            server.add_user_to_folder(projectname=projectname, username=new_admin_username)

            # change the admin in the database
            database.change_admin_of_project(projectname=projectname, email=email)
            # success
            return {"message": "admin for project: " + projectname + " is succefully changed to " + email}
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
  

# change scalability (max 4)
@app.patch("/project/scalability/{projectname}/{level}")
def change_scalability(projectname:str, level:int ):
    # check if projectname exist
    if not database.projectname_exists(projectname=projectname):
        raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )

    # check if number is not 0
    elif level == 0:
        raise HTTPException(
            status_code=400,
            detail="The level of scalability cannot be zero!"
        )
    
    # check if number is lower then 4
    elif level > 4:
           raise HTTPException(
            status_code=400,
            detail="The max. level is 4 (8 containers). If you want a higher availability please contact us: supportccs5@gmail.com "
        )
    
    # validation passed
    # change scalabilty
    else:
        try:
            # change the yaml file and restart pod
            server.change_scalabilty(projectname=projectname, level=level)

            # success
            return {"message": "You succesfully changed the scalability of project: "+ projectname }
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")

# remove user form the project
@app.delete("/project/remove/user/{projectname}/{email}")
def remove_user_from_project(projectname:str, email:str):
    # check if projectname exist
    if not database.projectname_exists(projectname=projectname):
        raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )
    
    # check if email exists
    elif not database.user_exists(email=email): 
         raise HTTPException(
            status_code=400,
            detail="The email that you chose does not exist! Please choose a valid email."
        )
    
    # validations passed
    # remove user from the user
    else:
        try:
            # remove from participation database
            database.delete_participation(projectname=projectname, email=email, role="user")
            # remove access to folder
            server.remove_user_from_folder(projectname=projectname, username=database.get_username(email=email))

            # successs
            return {"message": email + " no longer has access to project: "+ projectname}

        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")
    
# delete a project
@app.delete("/project/delete/{projectname}")
def delete_project(projectname:str):
    # check if project exists
    if not database.projectname_exists(projectname=projectname):
          raise HTTPException(
            status_code=400,
            detail="The project name that you chose does not exist! Please choose a valid project name."
        )
    # validations passed
    # delete project
    else:
        try:
            # delete project from database
            database.delete_project(projectname=projectname)

            # delete pod 
            server.delete_project(projectname=projectname)

            # delete directories
            server.delete_directories(projectname=projectname)

            # success
            return {"message":"Project with the name " + projectname + " was successfully deleted"}
        
        # catch the errors
        except:
            raise HTTPException(
                status_code=500,
                detail="Something went wrong on the server. Try again later or contact us: supportccs5@gmail.com")