# 0x14. MySQL

## Concepts
* Database administration
	* [What is a database](https://www.techtarget.com/searchdatamanagement/definition/database)
	* [What is a database primary/replicate cluster](https://www.digitalocean.com/community/tutorials/how-to-choose-a-redundancy-plan-to-ensure-high-availability#sql-replication)
	* [MySQL primary/replicate setup](https://www.digitalocean.com/community/tutorials/how-to-set-up-replication-in-mysql)
	* [Build a robust database backup strategy](https://www.databasejournal.com/ms-sql/developing-a-sql-server-backup-strategy/)

* [Web stack debugging](https://intranet.alxswe.com/concepts/68)
* [[How to] install mysql 5.7](https://intranet.alxswe.com/concepts/100002)

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

## [How to] Create a user in the primary DB for the replica server
Before you get started with your primary-replica synchronization, you need one more thing in place. On your primary MySQL server (web-01), create a new user for the replica server
The name of the new user should be replica_user, with the host name set to %, and can have whatever password you'd like.
`replica_user` must have the appropriate permission to replicate your primary MySQL server.

`holberton_user` will need `SELECT` privileges on the `mysql.user` table in order to check that `replica_user` was created with the correct permissions.

```sql
CREATE USER 'replica_user'@'%' IDENTIFIED BY 'replica_user';
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';
GRANT SELECT ON mysql.user TO 'holberton_user'@'localhost';
```

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
