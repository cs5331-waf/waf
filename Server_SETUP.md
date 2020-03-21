# Setup DVWA Server


## OS Specifications

- Ubuntu Desktop LTS 16.04 32-bit
- At least 1 GB RAM
- 20GB of Hard Disk

Note: Steps below may be applicable for 64-bit variants and Ubuntu Server 16.04.

## Procedure
Time Taken: Approx 30 minutes

### Update 

Update whatever is needed.

    sudo apt-get update
    sudo apt-get upgrade

### Install necessary packages
The following install command will prompt you to enter password for root account of mysql. It will be used later.

    sudo apt-get install apache2 php libapache2-mod-php mysql-server  php-mysql phpmyadmin

Install more packages (PHP Extensions + git):

    sudo apt install php-curl php-gd php-mbstring php-mcrypt php-xml php-xmlrpc git

### Get DVWA via Git

    cd /var/www/html
    sudo git clone https://github.com/ethicalhack3r/DVWA.git

### Create and Edit Config File

    sudo cp /var/www/html/DVWA/config/config.inc.php.dist  /var/www/html/DVWA/config/config.inc.php
Use whichever editor to edit the created configuration file. Vim is used below:

    sudo vim /var/www/html/DVWA/config/config.inc.php
Edit the following parameters:
```
$_DVWA = array();
$_DVWA[ 'db_server' ]   = 'localhost';
$_DVWA[ 'db_database' ] = 'dvwaDB';
$_DVWA[ 'db_user' ]     = 'dvwaUsr';
$_DVWA[ 'db_password' ] = 'dvwaP@ssw0rd';
```
The values `dvwaDB`, `dvwaUsr` and `dvwaP@ssw0rd` can be modified to your liking. They will be used when setting up mySQL.

### Set Permission for certain files and directories
Required for DVWA to work properly.

    sudo chown www-data:www-data /var/www/html/DVWA/hackable/uploads/
    sudo chown www-data:www-data /var/www/html/DVWA/external/phpids/0.6/lib/IDS/tmp/phpids_log.txt
    sudo chmod 757 /var/www/html/DVWA/config/

### Turn on PHP Permission
Set the php.ini file to set `allow_url_include = On` on line 840. If using vim,

    sudo vim /etc/php/7.0/apache2/php.ini +840

### Setup mySQL Database
Log into mySQL via root via the password you gave when installing mysql:
 

     mysql -u'root' -p

Execute the following commands in mySQL using the earlier values  `dvwaDB`, `dvwaUsr` and `dvwaP@ssw0rd`:

> CREATE DATABASE dvwaDB; 
> CREATE USER 'dvwaUsr'@'localhost' identified by 'dvwaP@ssw0rd';
> GRANT ALL PRIVILEGES ON dvwaDB.* TO 'dvwaUsr'@'localhost';
> FLUSH PRIVILEGES;
> exit

### Restart Apache

    sudo systemctl restart apache2.service


# Launch DVWA

Enter the following URL into your web browser:

    http://localhost/DVWA/

For first login:

    Username: admin
    Password: admin
Upon logging in, you should see the Setup Page **almost** similar to the following Setup. Ignore the reCAPTCHA Key; it is not needed.

![](https://miro.medium.com/max/1536/1*chPnoYmNi5HYG8GDT2fUdg.png)

Click on the specified button to be brought back to Login Page.
Second Login credentials:

    Username: admin
    Password: password

Upon logging in, you can try the activities.

## References

[https://medium.com/datadriveninvestor/setup-install-dvwa-into-your-linux-distribution-d76dc3b80357](https://medium.com/datadriveninvestor/setup-install-dvwa-into-your-linux-distribution-d76dc3b80357)

https://github.com/ethicalhack3r/DVWA/

https://askubuntu.com/questions/956268/how-do-i-setup-dvwa-on-ubuntu
