---
title: "Installing Roundcube Webmail on BlueOnyx 5209"
date: "2016-03-10"
description: "I recently had to migrate some older BlueOnyx and BlueQuartz servers to newer hardware and took the opportunity to install a newer webmail interface called Roundcube."
tags: ["BlueOnyx", "Roundcube"]
slug: "installing-roundcube-webmail-on-blueonyx-5209"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2016/03/10/installing-roundcube-webmail-on-blueonyx-5209"
permalink: "/post/2016/03/10/installing-roundcube-webmail-on-blueonyx-5209"
legacyPaths: ["/post/2016/03/10/installing-roundcube-webmail-on-blueonyx-5209"]
---
I recently had to migrate some older BlueOnyx and BlueQuartz servers to newer hardware and took the opportunity to install a newer webmail interface called Roundcube.

For those interested in the steps to install on the BlueOnyx 5209 hosting control panel that runs on CentOS 7 here are the instructions.

Here is a link to the same instructions but in txt format: [Roundcube Install.txt (8.21 kb)](/file.axd?file=/roundcube/Roundcube Install.txt)

Create a temporary folder to download the install to and download the roundcube install.

```bash
mkdir /home/downloads
cd /home/downloads
wget https://downloads.sourceforge.net/project/roundcubemail/roundcubemail/1.1.4/roundcubemail-1.1.4-complete.tar.gz
tar -xvzf roundcubemail-1.1.4-complete.tar.gz
```

Backup the php.conf file that BlueOnyx creates by default so that we can enable PHP on the web server and ensure that future updates to php.conf wont overwrite our changes.

```bash
cp /etc/httpd/conf.d/php.conf /etc/httpd/conf.d/php_enable.conf
nano -w /etc/httpd/conf.d/php_enable.conf
```

 Uncomment or add the following contents to the file

```xml
<FilesMatch \.php$>
    SetHandler application/x-httpd-php
</FilesMatch>
AddType text/html .php
DirectoryIndex index.php
```

Create a php test file

```html
nano -w /var/www/html/phpinfo.php
```

Add the following to the file

```
<? phpinfo(); ?>
```

 Login to the BlueOnyx interface and add the following paths to the PHP.INI settings. Security -> PHP Settings -> PHP.INI

```
/var/www/html
/etc/mail/
/var/log/roundcubemail/
```

Open a browser and see if the php information is displayed. If this steps works you are ready to move to the next step.

```
http://www.yourdomain.com/phpinfo.php
```

Install php-intl that is a pre-requisite for Roundcube

```bash
yum install php-intl
```

Move roundcube to the webserver folder

```html
cd /home/downloads
mv roundcubemail-1.1.4 /var/www/html/roundcubemail
```

You should now be able to access the web installer that will be used to generate the config.inc.php file.

```
http://www.yourdomain.com/roundcubemail/installer/
```

Follow the steps to select the configure the features you would like to enable. At the end it will return text that is to be put into the configuration file.

```bash
nano -w /var/www/html/roundcubemail/config/config.inc.php
```

Copy the configuration information to the open file.

The next step is optional but I added the following changes to the virtuser\_file.php file to remove the host information that is returned on the BlueOnyx server so that the users suggested email address does not include the host portion of the domain. For example sites on the box often start with @www.domain.com or @mail.domain.com and I only want them to be presented with @domain.com

```html
nano -w /var/www/html/roundcubemail/plugins/virtuser_file/virtuser_file.php

#Find the line that starts with this
if (count($arr) > 0 && strpos($arr[0], '@')) {

#Change the contents between the open and close brace to look like the following

if (count($arr) > 0 && strpos($arr[0], '@')) {

    if(strpos($arr[0], 'www.')){
        $arr[0] = str_replace('www.', '', $arr[0]);
    }
    else if(strpos($arr[0], 'users.')){
        $arr[0] = str_replace('users.', '', $arr[0]);
    }
    else if(strpos($arr[0], 'mail.')){
        $arr[0] - str_replace('mail.', '', $arr[0]);
    }

    $result[] = rcube_utils::idn_to_ascii(trim(str_replace('\\@', '@', $arr[0])));

    if ($p['first']) {
        $p['email'] = $result[0];
    break;
    }
}
```

Download infinitescroll plugin which creates a nice infinite scroll experience when paging through messages.

```bash
mkdir /var/www/html/roundcubemail/plugins/infinitescroll
cd /var/www/html/roundcubemail/plugins/infinitescroll
wget https://github.com/messagerie-melanie2/Roundcube-Plugin-Infinite-Scroll/archive/master.zip
unzip master.zip
mv ./Roundcube-Plugin-Infinite-Scroll-master/* .
rm Roundcube-Plugin-Infinite-Scroll-master/ -rf
rm master.zip
```

Create MySQL database

```
mysql -u root -p
CREATE DATABASE roundcubemail;
GRANT ALL PRIVILEGES ON roundcubemail.* TO roundcube@localhost IDENTIFIED BY 'cairngorm';
FLUSH PRIVILEGES;
exit
```

Import the roundcube database

```
mysql roundcubemail -u root -p < /var/www/html/roundcubemail/SQL/mysql.initial.sql
```

Setup /webmail alias so that all sites on the box can navigate to webmail by going to their domain ex: [www.yourdomain.com/webmail](http://www.yourdomain.com/webmail)

```bash
nano -w /etc/httpd/conf.d/roundcubemail.conf
Alias /webmail /var/www/html/roundcubemail
```

Restart the web server

```
service httpd restart
```

Now go to [www.yourdomain.com/webmail](http://www.yourdomain.com/webmail) and login to the Roundcube webmail interface.
