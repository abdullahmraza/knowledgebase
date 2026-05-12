# AppDynamics Java Agent Deployment

## Overview
This document explains how to deploy AppDynamics Java Agent for Java Applications

## Prerequisites
- Controller URL and access key

## Step-by-Step
1. Get latest appdynamics agent from Appdynamics sharepoint
2. Extract agent files
3. Configure controller-info.xml
4. Restart application

## Common Issues
- Agent not reporting → Check connectivity
- JVM crash → Verify compatibility

## Best Practices
- Instrument agent with the application user
- recursive permission for agent folder should be 755
