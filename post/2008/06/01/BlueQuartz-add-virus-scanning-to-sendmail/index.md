---
title: "BlueQuartz add virus scanning to sendmail"
date: "2008-06-01"
description: "This HowTo is designed to provide the simplest solution for virus scanning to a BlueQuartz box. However this will also work on any box running Redhat Enterprise Linux 4 or CentOS 4"
tags: ["Virus Scanning"]
slug: "bluequartz-add-virus-scanning-to-sendmail"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2008/06/01/BlueQuartz-add-virus-scanning-to-sendmail"
permalink: "/post/2008/06/01/BlueQuartz-add-virus-scanning-to-sendmail"
legacyPaths: ["/post/2008/06/01/BlueQuartz-add-virus-scanning-to-sendmail"]
---
This HowTo is designed to provide the simplest solution for virus scanning to a BlueQuartz box. However this will also work on any box running Redhat Enterprise Linux 4 or CentOS 4

 Note this uses a MILTER to scan for viruses and assumption is that you are not running any other MILTERS. If you are you will need to be smart enough to know how to modify the following instructions.

Assuming you dont have DAG or RPMFORGE installed which a basic box does not you will want to install the RPMFORGE repository so that you can easily install CLAMAV.

**Install RPMFORGE**

```
rpm -Uhv http://apt.sw.be/redhat/el4/en/i386/rpmforge/RPMS/rpmforge-release-0.3.6-1.el4.rf.i386.rpm
```

**Edit rpmforge.repo**

This is a safety step to ensure that you do not accidently update any of the following modules. Note however when we are done we will be disabling RPMFORGE as a secondary measure. Otherwise you could end updating modules specific to BlueQuartz that could cause issues.

```bash
nano -w /etc/yum.repos.d/rpmforge.repo
```

**Add the following line to your config**

exclude=yum\*,centos-yumconf\*,httpd\*,mod\_ssl\*,sendmail\*,procmail\*,imap\*,nss\_db\*,pam\*,pwdb\*,webalizer\*,sysklogd\*,proftpd\*

Should look something like the following. Save the file once completed.

# Name: RPMforge RPM Repository for Red Hat Enterprise 4 - dag
# URL: <http://rpmforge.net/>
[rpmforge]
name = Red Hat Enterprise $releasever - RPMforge.net - dag
#baseurl = <http://apt.sw.be/redhat/el4/en/$basearch/dag>
mirrorlist = <http://apt.sw.be/redhat/el4/en/mirrors-rpmforge>
#mirrorlist = <file:///etc/yum.repos.d/mirrors-rpmforge>
enabled = 1
protect = 0
gpgkey = <file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag>
gpgcheck = 1
exclude=yum\*,centos-yumconf\*,httpd\*,mod\_ssl\*,sendmail\*,procmail\*,imap\*,nss\_db\*,pam\*,pwdb\*,webalizer\*,sysklogd\*,proftpd\*

**Install ClamAV, ClamAV-Devel and ClamAV-Milter**

```bash
yum install clamav clamav-devel clamav-milter
```

This will display that it wants to include other needed packages. Says y to the prompt and it will download and install the packages.

**Disable rpmforge**

```
mv /etc/yum.repos.d/rpmforge.repo /etc/yum.repos.d/rpmforge.repo.bak
```

This will prevent this repository from being used in regular system updates. If you ever want to use the repository to install other modules you can simply copy it back to .repo and remove the .bak from the name.

**Backup sendmail configuration**

```
cp /etc/mail/sendmail.cf /etc/mail/sendmail.cf.bak
cp /etc/mail/sendmail.mc /etc/mail/sendmail.mc.bak
```

**Edit sendmail.mc to include milter**

```bash
nano -w /etc/mail/sendmail.mc
```

**Add mail filter lines to sendmail.mc just above confCACERT**

```
INPUT_MAIL_FILTER(`clmilter',`S=local:/var/clamav/clmilter.socket,T=S:4m;R:4m')dnl
define(`confINPUT_MAIL_FILTERS',`clmilter')dnl
```

**Example sendmail.mc modification**

TRUST\_AUTH\_MECH(`EXTERNAL DIGEST-MD5 CRAM-MD5 LOGIN PLAIN')dnl
define(`confAUTH\_MECHANISMS', `EXTERNAL GSSAPI DIGEST-MD5 CRAM-MD5 LOGIN PLAIN')dnl
dnl #
dnl # Rudimentary information on creating certificates for sendmail TLS:
dnl #     make -C /usr/share/ssl/certs usage
dnl #
INPUT\_MAIL\_FILTER(`clmilter',`S=local:/var/clamav/clmilter.socket,T=S:4m;R:4m')dnl
define(`confINPUT\_MAIL\_FILTERS',`clmilter')dnl
dnl #
define(`confCACERT\_PATH',`/usr/share/ssl/certs')
define(`confCACERT',`/usr/share/ssl/certs/ca-bundle.crt')
define(`confSERVER\_CERT',`/usr/share/ssl/certs/sendmail.pem')
define(`confSERVER\_KEY',`/usr/share/ssl/certs/sendmail.pem')
dnl #
dnl # This allows sendmail to use a keyfile that is shared with OpenLDAP's
dnl # slapd, which requires the file to be readble by group ldap
dnl #
dnl define(`confDONT\_BLAME\_SENDMAIL',`groupreadablekeyfile')dnl

**Save changes to file and update sendmail.cf**

```
cd /etc/mail/
make
```

**The installation is now complete.** You can either reboot your machine or issue these commands.

```
service clamd restart
service clamav-milter restart
service sendmail restart
```

**Verify installation is working**

```
tail -f /var/log/maillog
```

send an email to the system in question
You should see a message like the following

```
Jun  1 14:04:16 sandbox sendmail[4600]: m51L409D004600:
mailto:from=jscott@domain.com
, size=11, class=0, nrcpts=1, msgid=<
mailto:200806012104.m51L409D004600@sandbox2.10tohost.com
>, proto=SMTP, daemon=MTA, relay=192-168-105-5.domain.com [192.168.105.5] (may be forged)
Jun  1 14:04:17 sandbox sendmail[4600]: m51L409D004600: Milter add: header: X-Virus-Scanned: ClamAV version 0.93, clamav-milter version 0.93 on sandbox.domain.com
Jun  1 14:04:17 sandbox sendmail[4600]: m51L409D004600: Milter add: header: X-Virus-Status: Clean
Jun  1 14:04:17 sandbox sendmail[4604]: m51L409D004600: to=admin, delay=00:00:04, xdelay=00:00:00, mailer=local, pri=30479, dsn=2.0.0, stat=Sent
```

Other logs to take a look at:

Clamd Logs: /var/log/clamav/clamd.log
Freshclam Logs: /var/log/clamav/freshclam.log
