# Contribute

#Contributing
Here we will elaborate on some guidelines on how one can contribute to this project. Please feel free to ask more questions to clarify any details.
You can use the following channels of communication:
- [NYU DLTS Slack](https://nyu-dlts.slack.com): comments and questions for team members. Ask Kate for an invite.
- [UltraViolet tech email group](mailto:data-repository-tech@nyu.edu): Internal Google Group for team communications
#Git Flow
##Branching
Our Git flow is a simplified Git-Flow. Much like Git-Flow, we take advantage of a main branch, a development branch, and feature branches.
###The main Branch 
This branch remains readily deployable at all times. It has no end to its lifespan and only heavily tested code (or no code at all) is allowed in this exclusive branch. Any pull request to the main branch should be considered a new release.
###The development Branch 
This branch is where all ongoing work is done. It runs parallel to main and incorporates all bug fixes and features planned for specific release. When all planned features are implemented and the head of the development branch is tested and meets our coding requirements (to be discussed later) we are ready to create a PR to main.
###feature Branches 
feature branches branch off of development and must be merged back into development. A feature branch adds end-user functionality to the application. Each feature is described and discussed through the DLTS project tracking system (currently JIRA).  When working on a feature branch, it is important to only make changes that are relevant to the feature you are currently working on. Thus the lifespan of the feature branch is limited to the development of that feature. As a convention, we prefix feature branch names with the Jira ticket number.
###chore Branches 
chore branches branch off of development and must be merged back into development. A chore branch does not add end-user functionality but is used for housekeeping tasks (e.g., updating a configuration file). When working on a chore branch, it is important to only make changes that are relevant to the chore you are currently working on. Thus the lifespan of the chore branch is limited to the completion of the chore. As a convention, we prefix chore branch names with chore/ (e.g., chore/update-database-config).
###Hotfix Branches 
Hotfix branches are necessary in case we need an immediate fix in the current production system. Hotfix branches branch off of the main branch and must be merged back to development and main branches through pull request.


