---
title: "BlueQuartz enabling SSL/TLS FTP Support"
date: "2008-05-27"
description: "This is my first attempt at putting online a step by step process in support of the BlueQuartz server appliance."
tags: ["BlueQuartz", "Secure Ftp"]
slug: "bluequartz-enabling-ssl-tls-ftp-support"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2008/05/27/BlueQuartz-enabling-SSLTLS-Support"
permalink: "/post/2008/05/27/BlueQuartz-enabling-SSLTLS-Support"
legacyPaths: ["/post/2008/05/27/BlueQuartz-enabling-SSLTLS-Support"]
---
This is my first attempt at putting online a step by step process in support of the BlueQuartz server appliance.

**1)** See if you are running a version of proftpd that has mod\_tls.c module included

**Execute Statement**

```bash
 proftpd -i
```

Example Output: Note you are looking for mod\_tls.c to be included otherwise these instructions will not work for you.

[root@ruth ~]# proftpd -l
Compiled-in modules:
  mod\_core.c
  mod\_xfer.c
  mod\_auth\_unix.c
  mod\_auth\_file.c
  mod\_auth.c
  mod\_ls.c
  mod\_log.c
  mod\_site.c
  mod\_readme.c
  mod\_auth\_pam.c
  mod\_tls.c
  mod\_cap.c

**2)** Create SSL Certificate and directory to hold certificate

**Create Directory:**

```bash
 mkdir -p /etc/proftpd/ssl
```

**Create SSL Certificate:**

```bash
 openssl req -new -x509 \
 -days 365 \
 -nodes \
 -out /etc/proftpd/ssl/proftpd.cert.pem \
 -keyout /etc/proftpd/ssl/proftpd.key.pem
```

This will ask you a series of questions and generate the certificates

Country Name (2 letter code) [AU]: <-- Enter your Country Name (e.g., "US").
State or Province Name (full name) [Some-State]: <-- Enter your State or Province Name (eg., Washington).
Locality Name (eg, city) []: <-- Enter your City (e.g., "Seattle").
Organization Name (eg, company) [Internet Widgits Pty Ltd]: <-- Enter your Organization Name (e.g., the name of your company).
Organizational Unit Name (eg, section) []: <-- Enter your Organizational Unit Name (e.g. "IT Department").
Common Name (eg, YOUR name) []: <-- Enter the Fully Qualified Domain Name of the system (e.g. "server1.example.com").
Email Address []: <-- Enter your Email Address.


**3)** Edit /etc/proftpd.conf and add the text highlighted. Make note of placement in reference to existing configuration.

```bash
 nano -w /etc/proftpd.conf
```

<IfModule mod\_tls.c>
    TLSProtocol TLSv1
</IfModule>

# Restore file permissions capability to site administrator
 <Global>
   # Report localtime, not GMT
   TimesGMT                     off
   ServerIdent                  on "FTP Server"
   IdentLookups                 off

<IfModule mod\_tls.c>
    TLSEngine on
    TLSLog /var/log/tls.log

    # Are clients required to use FTP over TLS when talking to this server?
    TLSRequired off

    # Server's certificate
    TLSRSACertificateFile /etc/proftpd/ssl/proftpd.cert.pem
    TLSRSACertificateKeyFile /etc/proftpd/ssl/proftpd.key.pem

    # Authenticate clients that want to use FTP over TLS?
    TLSVerifyClient off

    # Allow SSL/TLS renegotiations when the client requests them, but
    # do not force the renegotations.  Some clients do not support
    # SSL/TLS renegotiations; when mod\_tls forces a renegotiation, these
    # clients will close the data connection, or there will be a timeout
    # on an idle data connection.
    TLSRenegotiate required off

</IfModule>

</Global>

4**)** Connect to server using a secure FTP client and choose FTP over Explicit SSL/TLS. If you dont have a secure FTP client try this free one FileZilla <http://filezilla-project.org/>
