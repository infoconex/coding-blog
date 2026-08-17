---
title: "Installing OpenWebmail on BlueOnyx server"
date: "2011-10-10"
description: "I have been in the process of evaluating the BlueOnyx distribution that replaces the older BlueQuartz web hosting control panel. However one of the short comings is that BlueOnyx does not currently incorporate a webmail…"
tags: []
slug: "installing-openwebmail-on-blueonyx-server"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2011/10/10/Installing-OpenWebmail-on-BlueOnyx-server"
permalink: "/post/2011/10/10/Installing-OpenWebmail-on-BlueOnyx-server"
legacyPaths: ["/post/2011/10/10/Installing-OpenWebmail-on-BlueOnyx-server"]
---
I have been in the process of evaluating the BlueOnyx distribution that replaces the older BlueQuartz web hosting control panel. However one of the short comings is that BlueOnyx does not currently incorporate a webmail interface.

So today I decided to work out what it would take to bring over Openwebmail to the BlueQuartz platform so that as I migrate users to the new platform they will have the same webmail interface that they have been used to. I will also be later installing RoundCube as a second webmail option but for now I want to maintain as much as possible backwards compatibility.

Here is the installation steps:

1) Grab the latest install of openwebmail from: <http://openwebmail.acatysmoof.com/>

- Note that I am installing version 2.5.3 however there are 2 versions currently available
  - [Official Version 2.5.3](http://openwebmail.acatysmoof.com/download/release)
  - [3.0 Beta 4](http://openwebmail.acatysmoof.com/download/current)

2) Download file to /var/www

- cd /var/www
- wget <http://openwebmail.acatysmoof.com/download/release/openwebmail-2.53.tar.gz>

3) Extract contents

- tar -xvzf openwebmail-2.53.tar.gz
- This will extract files to 2 different directories
  - /var/www/cgi-bin/openwebmail
  - /var/www/data/openwebmail

4) Change permissions on created folders

- chown root:mail /var/www/cgi-bin/openwebmail
- chown root:mail /var/www/data/openwebmail

5) Install Text::Iconv perl module required

- yum install perl-Text-Iconv

6) Add apache config file to set /webmail alias for openwebmail

- Create file /etc/http/config.d/httpd\_openwebmail.conf
- Place in file the contents of this file: [http\_openwebmail.conf](/file.axd?file=2011%2f10%2fhttp_openwebmail.conf)

7) Edit the openwebmail configuration file so that it reflects proper defaults

- nano -w /var/www/cgi-bin/openwebmail/etc/openwebmail.conf
- Edit these entries to look as follows.
  - ow\_cgidir                         /var/www/cgi-bin/openwebmail
  - ow\_cgiurl                         /openwebmail
  - ow\_htmldir                        /var/www/data/openwebmail
  - ow\_htmlurl                        /data/openwebmail
- Here is a complete example file that is from my system that reflects not only the above changes but other changes I make from the default to support our current user preferences.
- [openwebmail.conf](/file.axd?file=2011%2f10%2fopenwebmail.conf)
  - Note if you enable spell check like my above example configuration make sure you install the aspell library
  - yum install aspell
- You should open /var/www/cgi-bin/openwebmail/etc/openwebmail.conf.help if you want to understand all the possible settings that can be made

8) Edit dbm.conf

- nano -w /var/www/cgi-bin/openwebmail/etc/defaults/dbm.conf
- Change dbm\_ext     .db      to      dbm\_ext     .pag

9) Restart httpd

- /etc/init.d/httpd restart

10) Initialize openwebmail by running /var/www/cgi-bin/openwebmail/openwebmail-tool.pl --init

11) Finished - Open your browser and go to one of your websites located on the server and append /webmail to the url and if all is well you will have running webmail on your BlueOnyx machine.
