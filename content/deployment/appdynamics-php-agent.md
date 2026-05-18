# AppDynamics PHP Agent Deployment

## Overview
This document explains how to deploy AppDynamics PHP Agent for PHP Applications

## Prerequisites
- Controller URL and access key

## Step-by-Step

1. Run php -I to check the running php version
   
2. Run php -i | grep -e "Debug Build" and the response should be Debug Build = > no
   
3. mkdir /opt/appdynamics; mkdir /opt/appdynamics/phpagent; mkdir /opt/appdynamics/phpagent/proxy.communication; mkdir /opt/appdynamics/phpagent/logs
   
4. Navigate to the directory where we have copied php agent rpm on the server and execute below command
   APPD_CONF_CONTROLLER_HOST=appdsan1.services.conduent.com
   APPD_CONF_CONTROLLER_PORT=443 APPD_CONF_APP=HCI_Prod APPD_CONF_TIER=php
   APPD_CONF_NODE=HCIPCHPWEB01_10.105.176.9
   APPD_CONF_ACCOUNT_NAME=customer1
   APPD_CONF_ACCESS_KEY=cbea9406-40c3-4d94-a63b-e985aee7b278
   APPD_CONF_SSL_ENABLED=true
   APPD_PROXY_CTRL_DIR=/opt/appdynamics/phpagent/proxy.communication
   APPD_CONF_LOG_DIR=/opt/appdynamics/phpagent/logs/ sudo -E rpm -i appdynamics-php-agent.x86_64-23.11.0.839.rpm

5. Execute find / -name appdynamics_agent.ini to get the installed  location of php agent. There will be two appdynamics_agent.ini created. One under the installed location of the php agent, other would be the base location of the php application installed on the server.
   ![image](/static/media/php1.png)

6. Navigate to the php.d directory depending on the location where php is installed on the system, and edit newly created appdynamics_agent.ini file and add below lines in the file
   agent.cli_enabled = 1
   
   agent.auto_launch_proxy = 0
   
   agent.proxy_ctrl_dir = /opt/appdynamics/phpagent/proxy.communication
   ![image](/static/media/php2.png)

8. Navigate to php agent installed location, in our case it was /usr/lib/appdynamics-php-agent.
   ![image](/static/media/php3.png)
   Execute chmod 775 *
   
   Execute proxy/runProxy /opt/appdynamics/phpagent/proxy.communication /opt/appdynamics/phpagent/logs/ &

10. Execute ps -ef | grep proxy to check and confirm the running process from php agent.

11. Verify the newly created application on the appdynamics controller.
