---
title: "The CrowdStrike Outage Is a Reminder That Deployment Safety Matters"
date: "2024-07-20"
description: "The CrowdStrike outage is a reminder that even trusted software can cause enormous damage when an update goes wrong, and that staged rollouts and recovery plans matter."
tags: ["software engineering", "reliability", "deployments"]
slug: "the-crowdstrike-outage-is-a-reminder-that-deployment-safety-matters"
author: "Jim Scott"
permalink: "/post/2024/07/20/the-crowdstrike-outage-is-a-reminder-that-deployment-safety-matters"
---
The CrowdStrike outage this week is a pretty good reminder that even trusted software can cause a huge amount of damage when an update goes wrong.

The issue affected Windows systems around the world and disrupted airlines, banks, hospitals, and other businesses. Microsoft has estimated that about 8.5 million Windows devices were impacted.

What stands out to me is not just that a bad update happened. Software bugs happen.

The bigger issue is how quickly a problem can spread when software is deployed broadly and automatically.

For years we have pushed toward faster releases, more automation, and less manual intervention. Those are generally good things, but they also increase the importance of staged rollouts, testing, rollback plans, and having a way to stop an update before it reaches everyone.

The more critical the software, the more important those safeguards become.

This outage will probably be studied for a long time, but the basic lesson already seems pretty clear.

Getting software out quickly matters.

Being able to recover when something goes wrong matters even more.
