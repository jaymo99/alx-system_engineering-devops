# 0x14. MySQL

## Concepts
* Database administration
	* [What is a database](https://www.techtarget.com/searchdatamanagement/definition/database)
	* [What is a database primary/replicate cluster](https://www.digitalocean.com/community/tutorials/how-to-choose-a-redundancy-plan-to-ensure-high-availability#sql-replication)
	* [MySQL primary/replicate setup](https://www.digitalocean.com/community/tutorials/how-to-set-up-replication-in-mysql)
	* [Build a robust database backup strategy](https://www.databasejournal.com/ms-sql/developing-a-sql-server-backup-strategy/)

* [Web stack debugging](https://intranet.alxswe.com/concepts/68)
* [[How to] install mysql 5.7](https://intranet.alxswe.com/concepts/100002)

<br>
## [How to] install mysql 5.7

Copy the key here to your clipboard

[https://dev.mysql.com/doc/refman/5.7/en/checking-gpg-signature.html](https://dev.mysql.com/doc/refman/5.7/en/checking-gpg-signature.html)

Save it in a file on your machine i.e. `signature.key` and then
```bash
sudo apt-key add signature.key
```

add the apt repo
```bash
sudo sh -c 'echo "deb http://repo.mysql.com/apt/ubuntu bionic mysql-5.7" >> /etc/apt/sources.list.d/mysql.list'
```

update apt
```bash
sudo apt-get update
```

now check your available version:
```bash
vagrant@ubuntu-focal:/vagrant$ sudo apt-cache policy mysql-server
mysql-server:
  Installed: (none)
  Candidate: 8.0.27-0ubuntu0.20.04.1
  Version table:
     8.0.27-0ubuntu0.20.04.1 500
        500 http://archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu focal-security/main amd64 Packages
     8.0.19-0ubuntu5 500
        500 http://archive.ubuntu.com/ubuntu focal/main amd64 Packages
     5.7.37-1ubuntu18.04 500
        500 http://repo.mysql.com/apt/ubuntu bionic/mysql-5.7 amd64 Packages
```

Now install mysql 5.7
```bash
sudo apt install -f mysql-client=5.7* mysql-community-server=5.7* mysql-server=5.7*
```

<br>
## [How to] Create a DB user to allow the checker access
Create a MySQL user named `holberton_user` on both web-01 and web-02 with the host name set to `localhost` and the password `projectcorrection280hbtn`
```sql
CREATE USER 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';
```

Make sure that `holberton_user` has permission to check the primary/replica status of your databases.
```sql
GRANT REPLICATION CLIENT ON *.* TO 'holberton_user'@'localhost'
```

In order for you to set up replication, you’ll need to have a database with at least one table and one row in your primary MySQL server (web-01) to replicate from.
* Create a database named `tyrell_corp`
* Within tyrell_corp create a table named `nexus6` and add at lease one entry to it
```sql
CREATE DATABASE IF NOT EXISTS tyrell_corp;
USE tyrell_corp;
CREATE TABLE `nexus6` (
	`id` INT NOT NULL AUTO INCREMENT,
	`name` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`id`)
);

INSERT INTO `nexus6` (`name`) VALUES ('Leon');
	
```

Make sure that `holberton_user` has `SELECT` permissions on your table.
```sql
GRANT SELECT ON tyrell_corp.nexus6 TO 'holberton_user'@'localhost';
FLUSH PRIVILEGES;
```

<br>
## [How to] Create a user in the primary DB for the replica server
Before you get started with your primary-replica synchronization, you need one more thing in place. On your primary MySQL server (web-01), create a new user for the replica server
The name of the new user should be replica_user, with the host name set to %, and can have whatever password you'd like.
`replica_user` must have the appropriate permission to replicate your primary MySQL server.
At minimum, a MySQL replication user must have the `REPLICATION SLAVE` permissions:

`holberton_user` will need `SELECT` privileges on the `mysql.user` table in order to check that `replica_user` was created with the correct permissions.

It is a good practice to run the `FLUSH PRIVILEGES` command. This will free up any memory that the server cached as a result of the preceding `CREATE USER` AND `GRANT` statements.
```sql
CREATE USER 'replica_user'@'%' IDENTIFIED BY 'replica_user';
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';
GRANT SELECT ON mysql.user TO 'holberton_user'@'localhost';
FLUSH PRIVILEGES;
```

<br/>
Example output:

```bash
ubuntu@229-web-01:~$ mysql -uholberton_user -p -e 'SELECT user, Repl_slave_priv FROM mysql.user'
+------------------+-----------------+
| user             | Repl_slave_priv |
+------------------+-----------------+
| root             | Y               |
| mysql.session    | N               |
| mysql.sys        | N               |
| debian-sys-maint | Y               |
| holberton_user   | N               |
| replica_user     | Y               |
+------------------+-----------------+
ubuntu@229-web-01:~$

```

## [How to] Set up replication in MySQL
### Step 1. Allow incoming traffic on Source server's port 3306
This section assumes that you already have two Ubuntu servers, each installed with an instance of MySQL 5.7.*
You will have configured a firewall on both your servers with UFW. This will help to keep both your servers secure, but the source's firewall will block any connection attempts from your replica MySQL instance.
To change this, you’ll need to include a UFW rule that allows connections from your replica through the source’s firewall.

```bash
sudo ufw allow from <replica_server_ip> to any port 3306
```

### Step 2. Configure the source DB to begin replication
The default MySQL server configuration file is named `mysqld.cnf` and found in the `/etc/mysql/mysql.conf.d/` directory.
Open this file and find the `bind-address` directive. This directive instructs MySQL to only listen for connections on the `localhost` address. You need to comment out this paramenter

```
...
bind-address	= 127.0.0.1
...
```

Next find the `server-id` directive, used to distinguish servers in a replication setup.
This directive will be commented out by default and will look like this. You need to uncomment this line by remove the `#` character at the beginning.

```
...
# server-id 	= 1
...
```

Below the `server-id` line, find the `log_bin` directive. This defines the base name and location of MySQL's binary log file. Uncomment this line to enable binary loggin on the source server

```
...
log_bin 		= /var/log/mysql/mysql-bin.log
...
```

Lastly, scroll down to the bottom of the file to find the commented-out `binlog_do_db` directive. Remove the `#` sign to uncomment this line and replace `include_database_name` with the name of the database you want to replicate.

```
...
# binlog_do_db 	= <include_database_name>
...
```

Save and close the configuration file. Then restart the MySQL service

```bash
sudo systemctl restart mysql
```

With that, this MySQL instance is ready to function as the source database which your other MySQL server will replicate.

Use the link below to follow along with the next steps.

### [Next step - Retrieving Binary Log Coordinates from the Source](https://www.digitalocean.com/community/tutorials/how-to-set-up-replication-in-mysql#step-4-retrieving-binary-log-coordinates-from-the-source)























