import subprocess
import yaml
import database

### USER ###
# create a new user
def create_user(username:str, password:str):
    # Create the new user
    subprocess.run(['sudo', 'useradd', '-m', username])

    # Set the user's password
    subprocess.run(['sudo', 'chpasswd'], input=f"{username}:{password}", encoding='ascii')

# change user's password
def change_user_password(email:str, password:str):
    subprocess.run(['sudo', 'chpasswd'], input=f"{database.get_username(email)}:{password}", encoding='ascii')

# change user's name
def change_user_name(oldUsername:str, newUsername:str):
    # change username
    subprocess.run(["sudo", "usermod", "-l", newUsername, oldUsername])

    # change usergroup
    subprocess.run(["sudo", "groupmod", "-n", newUsername, oldUsername])


# change user's status
def change_user_status(username:str, status:int):
    # check if user needs to be actived (1) or deactived (0)
    if status == 1: # active
        subprocess.run(["sudo", "passwd", "-u", username])
    else: # deactive
        subprocess.run(["sudo", "passwd", "-l", username])

# delete a user
def delete_user_on_server(username:str):
    # delete user 
    subprocess.run(['sudo', 'userdel', '-r', username], check=True)

    # delete user group
    subprocess.run(['sudo', 'groupdel', '-r', username], check=True)
    
### DIRECTORIES ###
# create a new directories
def create_directorie_for_project(projectname:str):
    subprocess.run(["/home/ccs5/scripts/DirectoriesScripts/makeDirectories.sh " + projectname], shell=True)

# change permissions -> add user to folder
def add_user_to_folder(projectname: str, username:str):
    subprocess.run(["/home/ccs5/scripts/UserScripts/addUser.sh " + projectname + " " + username], shell=True)

# change permissions -> remove user from folder
def remove_user_from_folder(projectname:str, username:str):
    subprocess.run(["/home/ccs5/scripts/UserScripts/removeUser.sh " + projectname + " " + username], shell=True)

# delete directories
def delete_directories(projectname:str):
    # execute script to apply changes
    subprocess.run(["/home/ccs5/scripts/DirectoriesScripts/removeDirectories.sh " + projectname], shell=True)


### CREATE ALL YAMLS FOR PROJECT ###
# create project-namespace.yaml
def create_namespace_for_project(projectname:str):
    # path for the yaml file 
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    namespace_file = ""

    # get the default namespace file
    with open('/home/ccs5/cluster/templates/namespace.yaml', "r") as file:
        # load the yaml file locally
        namespace_file = yaml.safe_load(file)

        # change the metadata
        namespace_file["metadata"]["name"] = projectname

    # close the file
    file.close()
    
    # create the namespace file in the project directory
    with open(path + "-namespace.yaml", "w") as file:
        yaml.dump(namespace_file, file)

    # close file
    file.close()


# create project-deployment.yaml -> laravel
def create_deployment_laravel(projectname:str, databasename:str):
    # path for the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    deployment_file = ""

    # count variables
    env_count   = 0

    # get the default deployment file
    with open('/home/ccs5/cluster/templates/laravel.yaml', "r") as file:
        # load the yaml file locally
        deployment_file = yaml.safe_load(file)

        # change the metadata
        deployment_file["metadata"]["name"] = projectname + "-laravel-deployment"
        deployment_file["metadata"]["namespace"] = projectname

        # change app
        deployment_file["spec"]["selector"]["matchLabels"]["app"] = projectname
        deployment_file["spec"]["template"]["metadata"]["labels"]["app"] = projectname

        # change name of container
        deployment_file["spec"]["template"]["spec"]["containers"][0]["name"] = projectname + "-laravel"

        # loop thourgh env variables
        for variable in  deployment_file["spec"]["template"]["spec"]["containers"][0]["env"]:
            # 1st is link to mysql service
            if env_count == 0:
                variable["value"] = projectname + "-mysql-service"

            # 4th is the databasename
            if env_count == 3:
                variable["value"] = databasename

            # add to env count
            env_count += 1

        # change volume path
        deployment_file["spec"]["template"]["spec"]["volumes"][0]["nfs"]["path"] = "/projects/" + projectname + "/files"

    # close file
    file.close()

    # create the deployment file in the project directory
    with open(path + "-laravel-deployment.yaml", "w") as file:
        yaml.dump(deployment_file, file)
    
    # close file
    file.close()

def create_deployment_mysql(projectname:str, mysql:str):
    # path for the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    deployment_file = ""

    # count variables
    env_count   = 0

    # get the default deployment file
    with open('/home/ccs5/cluster/templates/mysql.yaml', "r") as file:
        # load the yaml file locally
        deployment_file = yaml.safe_load(file)

        # change the metadata
        deployment_file["metadata"]["name"] = projectname + "-mysql-deployment"
        deployment_file["metadata"]["namespace"] = projectname

        # change app
        deployment_file["spec"]["selector"]["matchLabels"]["app"] = projectname
        deployment_file["spec"]["template"]["metadata"]["labels"]["app"] = projectname

        # change the containername
        deployment_file["spec"]["template"]["spec"]["containers"][0]["name"] = projectname + "-mysql"

        # change the image 
        deployment_file["spec"]["template"]["spec"]["containers"][0]["image"] = "mysql:" + mysql

        # change volume
        deployment_file["spec"]["template"]["spec"]["volumes"][0]["persistentVolumeClaim"]["claimName"] = projectname +"-mysql-pvc"
    
    # close file
    file.close()

    # create the deployment file in the project directory
    with open(path + "-mysql-deployment.yaml", "w") as file:
        yaml.dump(deployment_file, file)
    
    # close file
    file.close()      



# create project-pv.yaml
def create_presistentVolume(projectname:str):
    # path for the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    pv_file = ""

    # get the default pvc file
    with open('/home/ccs5/cluster/templates/pv.yaml', "r") as file:
        # load the yaml file locally
        pv_file = yaml.safe_load(file)

        # change the metadata
        pv_file["metadata"]["name"] = projectname + "-mysql-pv"
        pv_file["metadata"]["namespace"] = projectname

        # change storage class name
        pv_file["spec"]["storageClassName"] = projectname + "-mysql-volume"

        # change the path to the nfs server
        pv_file["spec"]["nfs"]["path"] = "/projects/" + projectname + "/mysql"

    # close file
    file.close()

    # create the pvc file in the project directory
    with open(path + "-pv.yaml", "w") as file:
        yaml.dump(pv_file, file)

    # close file
    file.close()
    

# create project-pvc.yaml (persistentVolumeClaim)
def create_PersistentVolumeClaim(projectname:str):
    # path for the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    pvc_file = ""  

    # get the default pvc file
    with open('/home/ccs5/cluster/templates/pvc.yaml', "r") as file:
        # load the yaml file locally
        pvc_file = yaml.safe_load(file)

        # change the metadata
        pvc_file["metadata"]["name"] = projectname + "-mysql-pvc"
        pvc_file["metadata"]["namespace"] = projectname

        # change storage class name
        pvc_file["spec"]["storageClassName"] = projectname + "-mysql-volume"

        # change the volumename
        pvc_file["spec"]["volumeName"] = projectname + "-mysql-pv"

    # close file
    file.close()

    # create the pvc file in the project directory
    with open(path + "-pvc.yaml", "w") as file:
        yaml.dump(pvc_file, file)

    # close file
    file.close()

# create a laravel-service.yaml 
def create_service_laravel(projectname:str):
    # path for the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    service_file = ""  

    # get the default service file
    with open("/home/ccs5/cluster/templates/service.yaml", "r") as file:
        # load the yaml file locally
        service_file  = yaml.safe_load(file)

        # change metadata
        service_file["metadata"]["name"] = projectname + "-laravel-service" 
        service_file["metadata"]["namespace"] = projectname

    
    # close file
    file.close()

    # create the service file in the project directory
    with open(path + "-laravel-service.yaml", "w") as file:
        yaml.dump(service_file, file)

    # close file
    file.close()

# create a project-mysql-service.yaml
def create_service_mysql(projectname:str):
    # path for the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    service_file = ""  


    # get the default service file
    with open("/home/ccs5/cluster/templates/mysql-service.yaml", "r") as file:
        # load the yaml file locally
        service_file  = yaml.safe_load(file)

        # change the metadata
        service_file["metadata"]["name"] = projectname + "-mysql-service" 
        service_file["metadata"]["namespace"] = projectname

        # change app name
        service_file["spec"]["selector"]["app"] = projectname

    # close file
    file.close()

    # create the service file in the project directory
    with open(path + "-mysql-service.yaml", "w") as file:
        yaml.dump(service_file, file)

    # close file
    file.close()


# create a loadbalancer.yaml
def create_loadbalancer(projectname:str):
    # path to the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empyt yaml file
    loadbalancer_file = ""

    # get the file 
    with open("/home/ccs5/cluster/templates/loadbalancer.yaml", 'r') as file:
        # load the yaml file locally
        loadbalancer_file = yaml.safe_load(file)

        # change metadata
        loadbalancer_file["metadata"]["name"] = projectname + "-ingress"
        loadbalancer_file["metadata"]["namespace"] = projectname

        # change host
        loadbalancer_file["spec"]["rules"][0]["host"] = projectname + ".ccs5"

        # change paths 
        loadbalancer_file["spec"]["rules"][0]["http"]["paths"][0]["path"] = "/"+ projectname
        loadbalancer_file["spec"]["rules"][0]["http"]["paths"][0]["backend"]["service"]["name"] = projectname + "-laravel-service" 

    # close file
    file.close()

    # create the loadbalncer file in the project directory
    with open(path + "-loadbalancer.yaml", "w") as file:
        yaml.dump(loadbalancer_file, file)

    # close file
    file.close()


# create project on the cluster
def create_project(projectname: str):
    subprocess.run(["/home/ccs5/scripts/ProjectsScripts/startProject.sh " + projectname], shell=True)

# create new dns record
def create_DNS_record(projectname:str):
    # variables
    inventory_file = "/etc/ansible/inventory.yaml"
    playbook_file = "/etc/ansible/playbooks/addRecordDNS.yaml"
    user="ccs5"
    cmd= [
    "ansible-playbook",
    "-i", inventory_file,
    "-e", f"projectname={projectname}",
    "-u", user,
    playbook_file,]

    # change user and execute command
    subprocess.run(["sudo", "-u", user] + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



# delete project from the cluster
def delete_project(projectname:str):
    subprocess.run(["/home/ccs5/scripts/ProjectsScripts/removeProject.sh " +projectname], shell=True)

### PHP/MYSQL ###
PHPVERSIONS = ["7.0", "7.1", "7.2", "7.3", "7.4"]
MYSQLVERSIONS = ["5.7", "8.0", "latest"]

# validate the version
def validate_version(program: str, version:str):
    # check if php or mysql needs to be validate
    if program == "PHP": # PHP
        if version not in PHPVERSIONS:
            return False

    if program == "MYSQL": #MYSQL
        if version not in MYSQLVERSIONS:
            return False
    
    # unsuccesfull
    return True

# change the version of PHP/MYSQL
def change_version(projectname:str, application:str, version:str):
    # yaml file
    deployment_file = ""
    image = ""

    # check which app needs to be changed
    # mysql
    if application == "mysql":
        # path to the yaml file
        path = "/home/ccs5/projects/" + projectname + "/config/" + projectname + "-mysql-deployment.yaml"

        # create the image string
        image = "mysql:" + version

    # php
    elif application == "php":
         # path to the yaml file
        path = "/home/ccs5/projects/" + projectname + "/config/" + projectname + "-mysql-deployment.yaml"

        # create the image string
        image = "php:" + version + "-fpm"

    # open the yaml file
    with open(path, "r") as file:
        # load the file locally
        deployment_file = yaml.safe_load(file)
        
        # change the version
        deployment_file["spec"]["template"]["spec"]["containers"][0]["image"] = image

    # close the file
    file.close()

    # save the changes
    with open(path, "w") as file:
        yaml.dump(deployment_file, file)

    # close the file
    file.close()

    # execute script to apply changes
    subprocess.run(["/home/ccs5/scripts/DeploymentsScripts/updateDeployment.sh " + projectname + " " + application], shell=True)


### STATUS ###
# get the status of pods linked to a namespace
def get_pods_status(projectname:str):
    # execute script that get info from a pod the projectname is also the namespace
    pods_status = subprocess.check_output(["/home/ccs5/scripts/PodScripts/statusPod.sh " + projectname], shell=True)

    # we get a string from the script now we leave out the new line and create a list
    list_info_pods = pods_status.decode().replace("\n", "").split(" ")

    # variables
    output = []

    # loop to info to creat a output for every pod  for i in range len(list_info_pods):
    for i in range(0, len(list_info_pods), 3):
        # check ready 
        if list_info_pods[i+1] == "true":
            ready = 1
        else:
            ready = 0

        # create output for the pod and add it to final output
        output.append({"Podname": list_info_pods[i], "status": list_info_pods[i+2], "ready": str(ready) +"/1"})

    # return 
    return output


### SCALABILITY ###
def change_scalabilty(projectname:str, level:int):
    # variables
    replicas = 0
    deployment_file = ""

    # decide replicas
    if level == 1:
        replicas = 1
    elif level == 2:
        replicas = 2
    elif level == 3:
        replicas = 4
    else:
        replicas = 8

    # load the yaml file
    with open("/home/ccs5/projects/" + projectname + "/config/"+ projectname + "-deployment.yaml", "r") as file:
        # load the yaml file locally
        deployment_file  = yaml.safe_load(file)

        # change number of replications
        deployment_file["spec"]["replicas"] = replicas

    # close file
    file.close

    # change the yaml file
    with open("/home/ccs5/projects/" + projectname + "/config/"+ projectname + "-deployment.yaml", "w") as file:
        yaml.dump(deployment_file, file)

    # close file
    file.close()

    # execute script to apply changes
    subprocess.run(["/home/ccs5/scripts/DeploymentsScripts/updateDeployment.sh " + projectname], shell=True)


### TESTING ###
# create project-deployment.yaml -> demo -> testing
def create_deployment_for_project(projectname:str, php:str, mysql:str):
    # path for the yaml file
    path = "/home/ccs5/projects/" + projectname + "/config/" + projectname

    # create an empty yaml file
    deployment_file = ""

    # count variables
    container_count = 0
    volume_count = 0
    
    # get the default deployment file
    with open('/home/ccs5/cluster/templates/deployment.yaml', "r") as file:
        # load the yaml file locally
        deployment_file = yaml.safe_load(file)

        # change the metadata
        deployment_file["metadata"]["name"] = projectname + "-deployment"
        deployment_file["metadata"]["namespace"] = projectname

        # change app
        deployment_file["spec"]["selector"]["matchLabels"]["app"] = projectname
        deployment_file["spec"]["template"]["metadata"]["labels"]["app"] = projectname

        # loop through the containers
        for container in deployment_file["spec"]["template"]["spec"]["containers"]:
            # first container = nginx
            if container_count == 0:
                # change the name of the container
                container["name"] = projectname + "-nginx"

            # reset volume count 
            volume_count = 0
                    
            # second contianer = php
            if container_count == 1:
                # change the name of the container
                container["name"] = projectname + "-php"

                # change the version of the contianer
                container["image"] = "php:" + php +"-fpm"
        
            # third container = mysql
            if container_count == 2:
                # change the name of the container
                container["name"] = projectname + "-mysql"
                # change the version of the contianer
                container["image"] = "mysql:" + mysql
                container["volumeMounts"][0]["name"] = projectname + "-mysql-persistent-storage"

            # add to count
            container_count += 1
      
        # loop through the volumes
        for volume in deployment_file["spec"]["template"]["volumes"]:
            # normal files
            if volume_count == 0:
                volume["nfs"]["path"] = "/projects/" + projectname + "/files"

            # pvc
            if volume_count == 1:
                volume["name"] = projectname + "-mysql-persistent-storage"
                volume["persistentVolumeClaim"]["claimName"] = projectname +"-mysql-pvc"

            # add to count
            volume_count += 1

    # close file
    file.close()

    # create the deployment file in the project directory
    with open(path + "-deployment.yaml", "w") as file:
        yaml.dump(deployment_file, file)
    
    # close file
    file.close()