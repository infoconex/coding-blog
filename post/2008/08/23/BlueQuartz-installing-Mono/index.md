---
title: "BlueQuartz installing Mono"
date: "2008-08-23"
description: "Mono allows you to run applications written in .NET programming language on Linux machines."
tags: ["Mono"]
slug: "bluequartz-installing-mono"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2008/08/23/BlueQuartz-installing-Mono"
permalink: "/post/2008/08/23/BlueQuartz-installing-Mono"
legacyPaths: ["/post/2008/08/23/BlueQuartz-installing-Mono"]
---
Mono allows you to run applications written in .NET programming language on Linux machines.

**Historical note:** The Mono YUM repository URLs used by this 2008 procedure have been retired. The repository configuration below is preserved for historical context and should not be expected to work today.

**Step 1:** Install the YUM repository by grabbing the `mono.repo` file from the Mono website and placing it in the `/etc/yum.repos.d/` folder.

--- Update 7/22/2011 ---

The above file is no longer available. Here is the contents of the mono.repo file that I grabbed previously when it was available. Just take the contents and create a file in /etc/yum.repos.d/ called mono.repo with the following contents.

```ini
[mono]
name=Mono for rhel-4-i386 (stable)
# Historical Mono repository URL has been retired.
enabled=1
gpgcheck=0
```

**Step 2:** Install Mono by executing this command. yum install xsp

The above command should also install these required components

```text
Installing:
xsp                     noarch     1.9.1-0.novell   mono              210 k
Installing for dependencies:
mono-core               i586       1.9.1-2.novell   mono               17 M
mono-data               i586       1.9.1-2.novell   mono              1.8 M
mono-data-sqlite        i586       1.9.1-2.novell   mono              169 k
mono-nunit              i586       1.9.1-2.novell   mono              115 k
mono-web                i586       1.9.1-2.novell   mono              3.0 M
mono-winforms           i586       1.9.1-2.novell   mono              3.9 M
```

Congratulations you have installed mono and can now execute programs written in .NET on your machine. However I had you install XSP as it is a small webserver that can run a website written in .NET without having to integrate into your existing web application such as apache. If you want to integrate into apache follow the current [mod_mono documentation](https://www.mono-project.com/docs/web/mod_mono/).

**Setting up XSP**

**Step 1:** Create a folder that will be the root folder for your website. Example: **/home/monoweb/web**

**Step2:** Setup the startup script **/etc/rc.d/init.d/xsp** for XSP that will host your website. Change permissions to allow execute **chmod +x /etc/rc.d/init.d/xsp**  . Below you will find the example startup script I found on the web that has worked for me.

**Step 3:** Setup **/etc/xsp.conf** that the startup script uses to set the port and folder the website exists under.  Below is the example contents.

**Step 4:** Setup XSP to automatically start on reboots. **chkconfig xsp on**

**Step 5:** You are now ready to host your website. Simply publish your website files to the root folder you defined and issue this command **service xsp start**

**Contents of /etc/xsp.conf**

**Note:** you should change the --port definition to the port you want to use. Make sure nothing else is using the same port you define.

```text
--port 8082 --root /home/monoweb/web/
```

**Contents of /etc/rc.d/init.d/xsp**

**Historical script correction (October 2026):** The original example contained an inverted PID check and an escaped default `case` pattern. The script below fixes those issues, handles stale PID files, and checks whether `xsp2` exists. Shell syntax was checked with `bash -n` and `dash -n`; actual operation on the historical BlueQuartz environment was not tested.

```bash
#!/bin/sh
# Startup script for the historical XSP2 service
# chkconfig: 3 84 16
# description: XSP ASP.NET server

PIDFILE=/var/run/xsp.pid
XSP=/usr/bin/xsp2

. /etc/init.d/functions

start() {
    echo -n $"Starting xsp: "

    if [ -f "$PIDFILE" ]; then
        read -r pid < "$PIDFILE"
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo -n $"xsp is already running."
            failure
            echo
            return 1
        fi
        rm -f "$PIDFILE"
    fi

    if [ ! -x "$XSP" ]; then
        echo -n $"xsp2 executable not found."
        failure
        echo
        return 1
    fi

    ARGS=$(grep -v '^[[:space:]]*#' /etc/xsp.conf)
    # Intentional word splitting: xsp.conf contains command-line arguments.
    "$XSP" --nonstop $ARGS > /dev/null 2>&1 &
    pid=$!

    if kill -0 "$pid" 2>/dev/null; then
        echo "$pid" > "$PIDFILE"
        success
        echo
        return 0
    fi

    failure
    echo
    return 1
}

stop() {
    echo -n $"Shutting down xsp: "

    if [ ! -f "$PIDFILE" ]; then
        echo -n $"xsp is not running."
        failure
        echo
        return 1
    fi

    read -r pid < "$PIDFILE"
    if [ -z "$pid" ] || ! kill -0 "$pid" 2>/dev/null; then
        rm -f "$PIDFILE"
        echo -n $"xsp is not running."
        failure
        echo
        return 1
    fi

    if kill -15 "$pid"; then
        rm -f "$PIDFILE"
        success
        echo
        return 0
    fi

    failure
    echo
    return 1
}

restart() {
    stop || return $?
    start
}

case "$1" in
    start) start ;;
    stop) stop ;;
    restart) restart ;;
    *) echo "Usage: $0 {start|stop|restart}"; exit 1 ;;
esac

exit $?
```
