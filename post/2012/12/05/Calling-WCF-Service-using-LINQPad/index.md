---
title: "Calling WCF Service using LINQPad"
date: "2012-12-05"
description: "First, if you are a .NET developer and you are not using LINQPad yet go and check it out at www.linqpad.net . They offer a free version that is the same as the paid version but without intellisense and the pricing to up…"
tags: ["LINQPad", "WCF"]
slug: "calling-wcf-service-using-linqpad"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2012/12/05/Calling-WCF-Service-using-LINQPad"
permalink: "/post/2012/12/05/Calling-WCF-Service-using-LINQPad"
legacyPaths: ["/post/2012/12/05/Calling-WCF-Service-using-LINQPad"]
---
First, if you are a .NET developer and you are not using LINQPad yet go and check it out at [www.linqpad.net](http://www.linqpad.net). They offer a free version that is the same as the paid version but without intellisense and the pricing to upgrade to the full version is well worth the productivity gain you get.


Ok, with that out of the way let me get to the issue I came across and how I solved it.


**Issue:**


Created an assembly project in order to create a proxy to a web services using .NET Service Reference which I would then use in LINQPad to do some testing against my web service. Created a new linqpad script and added my reference to the assembly and wrote a method to call my web service. Upon executing I received an InvalidOperationException:


*Could not find default endpoint element that references contract 'WCFAcctMgmtWebServiceReference.AccountManagementWebservicesSoap' in the ServiceModel client configuration section. This might be because no configuration file was found for your application, or because no endpoint element matching this contract could be found in the client element.*


That is odd I can see that my assembly includes a file Proxy.exe.config that has the necessary service reference information


```xml
<system.serviceModel>
	<bindings>
		<basicHttpBinding>
			<binding name="AccountManagementWebservicesSoap" />
		</basicHttpBinding>
	</bindings>
	<client>
		<endpoint address="http://ws.domain.com/acctmgmt/v4/service.asmx"
			binding="basicHttpBinding" bindingConfiguration="AccountManagementWebservicesSoap"
			contract="WCFAcctMgmtWebServiceReference.AccountManagementWebservicesSoap"
			name="AccountManagementWebservicesSoap" />
	</client>
</system.serviceModel>
```


So why was it not working?


**Answer:**


Well it turns out that LINQPad needs to have this configuration information included in a file it uses since it is the application executing the proxy. At first glance one might assume they would place it in the the file included with LINQPad called LINQPad.exe.config but that would result in the same issue.


Instead you need to create a file in the same directory that LINQPad is installed in and name it linqpad.config


Adding the following to my new file resolved the issue


```xml
<?xml version="1.0" encoding="utf-8" ?>
<configuration>
	<system.serviceModel>
		<bindings>
			<basicHttpBinding>
				<binding name="AccountManagementWebservicesSoap" />
			</basicHttpBinding>
		</bindings>
		<client>
			<endpoint address="http://ws.domain.com/acctmgmt/v4/service.asmx"
				binding="basicHttpBinding" bindingConfiguration="AccountManagementWebservicesSoap"
				contract="WCFAcctMgmtWebServiceReference.AccountManagementWebservicesSoap"
				name="AccountManagementWebservicesSoap" />
		</client>
	</system.serviceModel>
</configuration>
```


Hopefully this article will save someone the time I spent figuring this out.
