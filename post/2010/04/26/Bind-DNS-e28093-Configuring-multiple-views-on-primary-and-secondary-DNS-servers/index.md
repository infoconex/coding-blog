---

title: "Bind DNS – Configuring multiple views on primary and secondary DNS servers"
date: "2010-04-26"
description: "If you have a firewall with DMZ and Internal zones and you have machines that sit behind the firewall that query DNS that resolves back to your machines inside one of those zones then it is…"
tags: []
slug: "bind-dns-configuring-multiple-views-on-primary-and-secondary-dns-servers"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2010/04/26/Bind-DNS-e28093-Configuring-multiple-views-on-primary-and-secondary-DNS-servers"
permalink: "/post/2010/04/26/Bind-DNS-e28093-Configuring-multiple-views-on-primary-and-secondary-DNS-servers"
legacyPaths: ["/post/2010/04/26/Bind-DNS-e28093-Configuring-multiple-views-on-primary-and-secondary-DNS-servers"]
---
If you have a firewall with DMZ and Internal zones and you have machines that sit behind the firewall that query DNS that resolves back to your machines inside one of those zones then it is likely that you have had to setup some type of DNS configuration that allows internal hosts to resolve a DNS name to the internal IP rather than the public IP address.

Now you could do that by creating hosts entries on each machine so that it does not use DNS to resolve the machine name, or you could setup a set of DNS servers for internal machines to use that only host internal DNS. However that complicates things and makes it very hard to maintain.

If you are using BIND DNS then you have an option called Views. Views allow you to create zones  that will return different information based on the IP address or range of IP addresses that are querying. However getting this configuration right can be a little tricky as my experience it researching the topic resulted in lots of bad information.

So I am attempting to create an article that hopefully will help the next person who needs to set this up.

So lets take a look at views. A view as defined by the creator of BIND is “The **view** statement is a powerful feature of BIND 9 that lets a name server answer a DNS query differently depending on who is asking. …. Each **view** statement defines a view of the DNS namespace that will be seen by a subset of clients. A client matches a view if its source IP address matches the `address_match_list` of the view's **match-clients** clause ”

This looks like it will accomplish exactly what we want. So let me provide an example scenario to help us walk through the configuration.

We will be setting up 2 DNS servers. One of the servers will act as our primary (master) server and the other as a secondary (slave) server. The master is were all DNS changes will be made to our zones and those changes will then get propagated to the slave server. We want DNS servers and clients on the public internet to be able to query for our zones and get returned to them the public IP information. However the servers and machines inside our firewall should have returned to them the internal IP addresses when querying the same zone.

I am attaching the two named.conf files that are referenced below.

[Master Server  named.conf](/file.axd?file=2010%2f4%2fmaster.txt "Master named.conf")

[Secondary named.conf](/file.axd?file=2010%2f4%2fslave.txt "Secondary named.conf")

The following information is fictitious and only used to create this example.

**External Network:** 74.125.127.0/24

**Internal Network:** 192.168.1.0/24

**Domain:** mydomain.com

So lets assume our external zone should look like the following.

> $ttl 38400
> mydomain.com.   IN      SOA     dns1.mydomain.com. postmaster.mydomain.com. (
>                         1271863698
>                         10800
>                         3600
>                         604800
>                         38400 )
> mydomain.com.   IN      NS      dns1.mydomain.com.
> mydomain.com.   IN      NS      dns2.mydomain.com.
>
> dns1.mydomain.com.     IN      A       74.125.127.10
> dns2.mydomain.com.     IN      A       74.125.127.11
>
> mail.mydomain.com.      IN      A       74.125.127.5
> mydomain.com.   IN      MX      10 mail.mydomain.com.
>
> [www.mydomain.com](http://www.mydomain.com)     IN      A       74.125.127.6

and our internal zone looks like this

> $ttl 38400
> mydomain.com.   IN      SOA     dns1.mydomain.com. postmaster.mydomain.com. (
>                         1271863698
>                         10800
>                         3600
>                         604800
>                         38400 )
> mydomain.com.   IN      NS      dns1.mydomain.com.
> mydomain.com.   IN      NS      dns2.mydomain.com.
>
> dns1.mydomain.com.     IN      A       192.168.1.10
> dns2.mydomain.com.     IN      A       192.168.1.11
>
> mail.mydomain.com.      IN      A       192.168.1.5
> mydomain.com.   IN      MX      10 mail.mydomain.com.
>
> [www.mydomain.com](http://www.mydomain.com)     IN      A       192.168.1.6

So what we want to happen is that if a client on the internet queries for [www.mydomain.com](http://www.mydomain.com) they will get 74.125.127.6 and if anything behind the firewall queries for [www.mydomain.com](http://www.mydomain.com) they will get the internal IP 192.168.1.6

**MASTER SERVER**

So lets take a look at the named.conf on our master server and see how it looks.

We first create some acl entries that will make it easier to configure some of our options by using a friendly name that contains a list of IP addresses.

The first ACL “dns\_slaves” will be used to hold the IP addresses we will use on our secondary servers. Notice that it has two IP addresses .11 and .12. This is because later we will be configuring our secondary server with 2 IP addresses to allow it to use a different source IP address for queries to the master server based on if we are getting external or internal zone information.

acl "dns\_slaves" {
        192.168.1.11;
        192.168.1.12;
};

The ACL “internal\_slave” is the IP address that will be used by the secondary DNS server to query for internal zone information

acl "internal\_slave" {
        192.168.1.11;
};

The ACL “external\_slave” is the IP address that will be used by the secondary DNS server to query for external zone information

acl "external\_slave" {
        192.168.1.12;
};

The ACL “internal\_hosts” represents the IP range of our internal network that queries will come from

acl "internal\_hosts" {
        192.168.1.0/24;
};

options allows us to define global defaults for all zones and views. The two options that are important are the allow-query { any; } which allows by default any client to query the zone mydomain.com and any others we may decide to host in our DNS servers. The next important settings is recursion setting which we have defaulted to no. Recursion allows clients to query a DNS server for any domain that the server is not responsible for and get back DNS information. Since we do not want the world to use our DNS servers except when resolving our domains we have set this by default to no. Later we will override that setting for clients behind the firewall since they will be using the DNS server to also resolve other domains.

options {
        directory "/etc";
        pid-file "/var/run/named/named.pid";
        allow-query { any; };
        recursion no;
};

Now here is the configuration for our internal view.

match-clients - Since the internal view should only be used by IP addresses querying from inside our network the match-clients has two entries. !external\_slave which will block a query coming from the slave server IP that is used for the external zone and an entry matching our internal\_hosts acl which is any IP address in that acl range. Note that since we do not have any other acl anything else is automatically denied.

recursion –Set to yes so that internal clients can do recursive lookups using this server.

allow-transfer - Set to internal\_slave so that the secondary can request transfers for this views zones.

also-notify - Set to the IP address of the secondary server. For some reason BIND does not allow you use an ACL when setting this entry. This is also not necessary to add but I found it made it very explicit. By default BIND will use the DNS entries listed for the zone.

zone mydomain.com - Simply defines that it is a master zone.

view "internal" {

        match-clients {
                !external\_slave;
                internal\_hosts;
        };

        recursion yes;

        allow-transfer {
                internal\_slave;
        };

        also-notify {
                192.168.1.11;
        };

        zone "." {
                type hint;
                file "/var/named/root.internal";
        };
        zone "localhost" {
                type master;
                file "/var/named/localhost.internal.hosts";
        };
        zone "1.0.0.127.in-addr.arpa" {
                type master;
                file "/var/named/127.0.0.1.internal.rev";
        };
         zone "mydomain.com" {
                type master;
                file "/var/named/mydomain.com.internal";
        };

};

Now we jump to our external view

match-clients – Matches a query from external\_slave which is the IP address that will be used by the slave server to query for zone information to the primary server. !internal\_hosts excludes any other IP address internal from querying the zones in external and the last statement any allows all other IP’s to match the view.

recursion – Set to no so that no external clients can use the DNS server for recursive queries

allow-transfer – Set to allow the IP of the slave server assigned for external view to make zone transfers

also-notify – Set to IP of secondary to notify it of zone updates

zone mydomain.com – points to file containing the internal zone information

view "external" {

        match-clients {
                external\_slave;
                !internal\_hosts;
                any;
        };

        recursion no;

        allow-transfer {
                external\_slave;
        };

        also-notify {
                192.168.1.12;
        };

        zone "mydomain.com" {
                type master;
                file "/var/named/mydomain.com.external";
        };

};

So that finishes up our primary (master) server confirmation. In summary our master has two views “Internal” and “External” which hosts different zone files based on the clients that will query it. If someone queries and matches our “External” view they will get the public IP addresses. If someone queries and matches our “Internal” view they will get the private IP addresses.

**SECONDARY SERVER**

ACL entries

dns\_master is the IP address of the master server

acl dns\_masters {
        192.168.1.10;
        };

internal\_hosts is our internal ip range

acl internal\_hosts {
        192.168.1.0/24;
        };

options has two entries that are important. allow-query {any;} which allows any IP to query the zones we host and recursion no to not allow by default recursive lookups.

options {
        directory "/etc";
        pid-file "/var/run/named/named.pid";
        allow-query { any; };
        recursion no;
};

Here is our internal view

match-clients – Set to internal\_hosts to only allow IP addresses inside the network to match the view

recursion – Set to yes to allow internal clients recursive lookup capabilities

zone mydomain.com – This is the important part. Notice that transfer-source is set to 192.168.1.11. This forces the zone transfer request to come from the IP 192.168.1.11. When the master server see’s the query coming from that IP it will match the internal view and transfer the correct zone information for mydomain.com that matches the internal zone.

view "internal" {

        match-clients {
                internal\_hosts;
                };

        recursion yes;

        allow-notify {
                dns\_masters;
                };

        zone "." {
                type hint;
                file "/var/named/root.internal";
                };

        zone "localhost" {
                type master;
                file "/var/named/localhost.internal.hosts";
                };
        zone "1.0.0.127.in-addr.arpa" {
                type master;
                file "/var/named/127.0.0.1.internal.rev";
                };

        zone "mydomain.com" {
                type slave;
                masters { 192.168.1.10; };
                transfer-source 192.168.1.11
                file "/var/named/slaves/mydomain.com.internal";
        };
};

External View

match-clients - !internal\_hosts prevents internal IP’s from getting external view and matches everything else due to the any statement.

recursion – Set to no so that external clients are not able to perform recursive lookups.

allow-notify – Set to dns\_masters to allow notifications from the master server

zone mydomain.com - This is the important part. Notice that transfer-source is set to 192.168.1.12. This forces the zone transfer request to come from the IP 192.168.1.12. When the master server see’s the query coming from that IP it will match the internal view and transfer the correct zone information for mydomain.com that matches the internal zone.

view "external" {

        match-clients {
                !internal\_hosts;
                any;
                };

        recursion no;

        allow-notify {
                dns\_masters;
                };

        zone "mydomain.com" {
                type slave;
                masters { 192.168.1.10; };
                transfer-source 192.168.1.12;
                file "/var/named/slaves/mydomain.com.external";
        };

};
