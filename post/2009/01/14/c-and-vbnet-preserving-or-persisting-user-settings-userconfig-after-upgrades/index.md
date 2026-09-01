---

title: "c# and vb.net preserving or persisting user settings user.config after upgrades"
date: "2009-01-14"
description: "If you store settings in your application using Settings.Settings and have ever upgraded your application you may have found all the user settings have vanished."
tags: []
slug: "c-and-vb-net-preserving-or-persisting-user-settings-user-config-after-upgrades"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/01/14/c-and-vbnet-preserving-or-persisting-user-settings-userconfig-after-upgrades"
permalink: "/post/2009/01/14/c-and-vbnet-preserving-or-persisting-user-settings-userconfig-after-upgrades"
legacyPaths: ["/post/2009/01/14/c-and-vbnet-preserving-or-persisting-user-settings-userconfig-after-upgrades"]
---
If you store settings in your application using Settings.Settings and have ever upgraded your application you may have found all the user settings have vanished. It seems that the user.config file is stored in %UserProfile/LocalSettings/Application Data/CompanyName/ApplicationName/versionnumber/user.config

Every time you increment the version on your application a new version folder will be created that is of course empty and the process of populating those user specific settings starts over again.

Here is a way you can use to persist those settings after an upgrade.

C# Directions:

In your project open Settings.Settings and add a new user setting called ShouldUpgrade and set this to be a boolean value and set the value to **true**. Now click View Code icon at the top left side of the settings window. In the constructor add something like this.

public Settings()
{
    if(this.ShouldUpgrade)
    {
        this.Upgrade();
        this.ShouldUpgrade = false;
        this.Save();
    }
}

So the first time that the settings class is instantiated it will check the ShouldUpgrade setting of the new user.config file which will be set to true. The this.Upgrade() then copies any user settings from the most recent version prior to this upgrade. Then set ShouldUpgrade to false and save the settings.

Also because we stored ShouldUpgrade as a user setting this upgrade will happen for each individual user on the same machine.

For VB.NET you do the same approach but use My.Settings.Upgrade()
