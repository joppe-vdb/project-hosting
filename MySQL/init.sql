CREATE TABLE IF NOT EXISTS users(
        user_id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(45) NOT NULL,
        password VARCHAR(120) NOT NULL,
        email VARCHAR(120) NOT NULL,
        username VARCHAR(80) NOT NULL,
        active BOOLEAN DEFAULT true,
        PRIMARY KEY (user_id),
        UNIQUE (email),
        UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS projects(
        project_id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(45),
        phpVersion VARCHAR(45),
        mysqlVersion VARCHAR(45),
        admin_id INT,
        scalability INT,
        PRIMARY KEY (project_id)
);


CREATE TABLE IF NOT EXISTS participations(
        participation_id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL,
        project_id INT NOT NULL,
        role VARCHAR(30),
        PRIMARY KEY (participation_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


CREATE TABLE IF NOT EXISTS machines {
        machines_id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(30) NOT NULL,
        ip VARCHAR(40) NOT NULL,
        status VARCHAR(40) NOT NULL,
        function VARCHAR(150)
}

