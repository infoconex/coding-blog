---

title: "Validating your SSL certificate is properly installed for SMTP - POP3 - IMAP - HTTP"
date: "2016-03-16"
description: "I recently installed a new SSL certificate on one of my Linux boxes and wanted to verify that my email server was using the new certificate."
tags: ["SSL", "Linux"]
slug: "validating-your-ssl-certificate-is-properly-installed-for-smtp-pop3-imap-http"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2016/03/16/validating-your-ssl-certificate-is-properly-installed-for-smtp-pop3-imap-http"
permalink: "/post/2016/03/16/validating-your-ssl-certificate-is-properly-installed-for-smtp-pop3-imap-http"
legacyPaths: ["/post/2016/03/16/validating-your-ssl-certificate-is-properly-installed-for-smtp-pop3-imap-http"]
---
I recently installed a new SSL certificate on one of my Linux boxes and wanted to verify that my email server was using the new certificate. For HTTP this can be easy as you simply go to the secure URL and check your browsers SSL Icon to see that the certificate is as expected. However for SMTP, POP3 and IMAP I was not aware of a similar way to verify.

After some research I found that you can validate using a feature built into OpenSSL

**Secure SMTP**

openssl s\_client -showcerts -starttls smtp -crlf -connect localhost:587

**Secure IMAP**

openssl s\_client -showcerts  -crlf -connect localhost:993

**Secure POP3**

openssl s\_client -showcerts  -crlf -connect localhost:995

**Secure HTTP**

openssl s\_client -showcerts  -crlf -connect localhost:443

This will return something like the following that you can then use to verify your SSL certificate is installed properly

```html
CONNECTED(00000003)
depth=0 OU = Domain Control Validated, OU = PositiveSSL, CN = c1.infoconex.com
verify error:num=20:unable to get local issuer certificate
verify return:1
depth=0 OU = Domain Control Validated, OU = PositiveSSL, CN = c1.domain.com

---
Certificate chain
 0 s:/OU=Domain Control Validated/OU=PositiveSSL/CN=c1.domain.com
   i:/C=GB/ST=Greater Manchester/L=Salford/O=COMODO CA Limited/CN=COMODO RSA Domain Validation Secure Server CA
```
