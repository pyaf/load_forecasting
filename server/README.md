# Django Source code for website


## MySQL setup
	
	# Install dependencies

	sudo apt-get update
	sudo apt-get install mysql-server python3-dev libmysqlclient-dev
	pip install mysqlclient

	# MySQL database setup
	# verify that mysql service is running

	systemctl status mysql.service
	
	# if mysql not running, run : sudo systemctl start mysql
	
	mysql -u root -p
	CREATE DATABASE db_name CHARACTER SET UTF8;

	# check databases by 'show databases;'
	
	CREATE USER db_user@localhost IDENTIFIED BY 'userpassword';
	GRANT ALL PRIVILEGES ON db_name.* TO db_user@localhost;
	FLUSH PRIVILEGES;
	exit


	# Now create a file, /etc/mysql/db.cnf and add following content

	[client]
	database = db_name
	user = db_user
	password = userpassword
	default-character-set = utf8

#for Completetly removing mysql
	sudo service mysql stop  #or mysqld
	sudo killall -9 mysql
	sudo killall -9 mysqld
	sudo apt-get remove --purge mysql-server mysql-client mysql-common
	sudo apt-get autoremove
	sudo apt-get autoclean
	sudo deluser mysql
	sudo rm -rf /var/lib/mysql
	sudo apt-get purge mysql-server-core-5.7
	sudo apt-get purge mysql-client-core-5.7
	sudo rm -rf /var/log/mysql
	sudo rm -rf /etc/mysql 


