FROM gitlab/gitlab-ce:latest
RUN apt-get update && apt-get install apache2 -y \
        && apt-get install php7.0 -y \
        && apt-get install libapache2-mod-php7.4 -y \
        && apt-get install php7.4-mysql -y \
        && apt-get install mysql-server -y \
        #&& service mysql start \
        && mysql -u root -e "CREATE USER 'wordpress'@'%' IDENTIFIED BY '123456';GRANT ALL ON *.* TO 'wordpress'@'%';" \
        && mysql -u wordpress -p123456 -e "create database wordpress" \
        && wget https://wordpress.org/latest.zip \
        && unzip latest.zip \
        && mkdir /var/www/html/wp \
        && mv wordpress/* /var/www/html/wp \
        && chmod -R 777 /var/www/html/ \
        && cp /var/www/html/wp/wp-config-sample.php /var/www/html/wp/wp-config.php \
        && sed -i 's/database_name_here/wordpress/g' /var/www/html/wp/wp-config.php \
        && sed -i 's/username_here/wordpress/g' /var/www/html/wp/wp-config.php \
        && sed -i 's/password_here/123456/g' /var/www/html/wp/wp-config.php \
        && sed -i 's/80/81/g' /etc/apache2/ports.conf \
        #&& service apache2 restart \
