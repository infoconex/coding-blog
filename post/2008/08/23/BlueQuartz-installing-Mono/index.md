---
title: "BlueQuartz installing Mono"
date: "2008-08-23"
description: "Mono allows you to run applications written in .NET programming language on Linux machines."
tags: ["mono"]
slug: "bluequartz-installing-mono"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2008/08/23/BlueQuartz-installing-Mono"
permalink: "/post/2008/08/23/BlueQuartz-installing-Mono"
legacyPaths: ["/post/2008/08/23/BlueQuartz-installing-Mono"]
---
Mono allows you to run applications written in .NET programming language on Linux machines.

**Step 1:** Install the YUM repository by grabbing the file [mono.repo](http://www.go-mono.com/download/fedora-3-i386/mono.repo) from the mono website and placing in /etc/yum.repos.d/ folder.

--- Update 7/22/2011 ---

The above file is no longer available. Here is the contents of the mono.repo file that I grabbed previously when it was available. Just take the contents and create a file in /etc/yum.repos.d/ called mono.repo with the following contents.

 [mono]
name=Mono for rhel-4-i386 (stable)
baseurl=http://go-mono.com/download-stable/rhel-4-i386/
enabled=1
gpgcheck=0

**Step 2:** Install Mono by executing this command. yum install xsp

The above command should also install these required components

Installing:
xsp                     noarch     1.9.1-0.novell   mono              210 k
Installing for dependencies:
mono-core               i586       1.9.1-2.novell   mono               17 M
mono-data               i586       1.9.1-2.novell   mono              1.8 M
mono-data-sqlite        i586       1.9.1-2.novell   mono              169 k
mono-nunit              i586       1.9.1-2.novell   mono              115 k
mono-web                i586       1.9.1-2.novell   mono              3.0 M
mono-winforms           i586       1.9.1-2.novell   mono              3.9 M

Congratulations you have installed mono and can now execute programs written in .NET on your machine. However I had you install XSP as it is a small webserver that can run a website written in .NET without having to integrate into your existing web application such as apache. If you want to integrate into apache follow the instructions at this [Mono website](http://www.mono-project.com/Mod_mono).

**Setting up XSP**

**Step 1:** Create a folder that will be the root folder for your website. Example: **/home/monoweb/web**

**Step2:** Setup the startup script **/etc/rc.d/init.d/xsp** for XSP that will host your website. Change permissions to allow execute **chmod +x /etc/rc.d/init.d/xsp**  . Below you will find the example startup script I found on the web that has worked for me.

**Step 3:** Setup **/etc/xsp.conf** that the startup script uses to set the port and folder the website exists under.  Below is the example contents.

**Step 4:** Setup XSP to automatically start on reboots. **chkconfig xsp on**

**Step 5:** You are now ready to host your website. Simply publish your website files to the root folder you defined and issue this command **service xsp start**

**Contents of /etc/xsp.conf**

**Note:** you should change the --port definition to the port you want to use. Make sure nothing else is using the same port you define.

--port 8082 --root /home/monoweb/web/

**Contents of /etc/rc.d/init.d/xsp**

#!/bin/sh
#
# Startup script for xsp server
#
# chkconfig: 3 84 16
# description: xsp is a asp.net server
#
ARGS=`cat /etc/xsp.conf | grep -v \# `

. /etc/init.d/functions

start() {
echo -n $"Starting xsp: "
# Check PID/existence
pid=""
if [ -f /var/run/xsp.pid ] ; then
         read pid < /var/run/xsp.pid
         if [ -n "$pid" ]; then
   rm /var/run/xsp.pid
  else
   echo -n $"xsp is already running."
   failure
   echo
   return 1
         fi
fi

/usr/bin/xsp2 --nonstop $ARGS > /dev/null &
RETVAL=$?
if [ $RETVAL != 0 ]; then
  failure
  echo
  return $RETVAL
  fi
PID=$!
echo $PID > /var/run/xsp.pid
success
echo
return 0
}

stop() {
echo -n $"Shutting down xsp: "

if [ ! -f /var/run/xsp.pid ]; then
  echo -n $"xsp not running"
  failure
  echo
  return 1
fi

kill -15 `cat /var/run/xsp.pid`
RETVAL=$?

if [ $RETVAL = 0 ]; then
  rm /var/run/xsp.pid
  success
  echo
  return 0
else
  failure
  echo
  return $RETVAL
fi
}

restart() {
stop
start
}

case "$1" in
  start)
   start
;;
  stop)
   stop
;;
  restart)
   restart
;;
  \*)
echo $"Usage: $0 {start|stop|restart}"
exit 1
esac

exit $?
