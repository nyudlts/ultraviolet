---
layout: default
title: User Roles
parent: Project Orientation
nav_order: 3
has_toc: true

---
# {{ page.title }}


## User Roles

Ultraviolet has a series of user roles by default that allow us to test the permissions factory.  This page is an overview of the default roles in Ultraviolet and a description of how the correspond to the NYU use case users. Login with these credentials for local testing and development.

### Admin SuperUser
- Login: admin@test.com
- Password: adminpassword
- Purpose: all permissions to do anything in the system.

### NYU Depositor
- Login: nyudepositor@test.com
- Password: nyudepositor
- Purpose: can see files for anything restricted to NYU
Permissions to deposit files and create records.

### NYU Viewer
- Login: nyuviewer@test.com
- Password: nyuviewer
- Purpose: Can see files for anything restricted to NYU

### Restricted Data User
- Login: restdatauser@test.com
- Password: restdatauser
- Purpose: User who has agreed to terms of data use
User can access a specific record for which they have agreed to terms of use

### Public Viewer
- Login: publicviewer@test.com
- Password: publicviewer
- Purpose: Can see any files that are open
