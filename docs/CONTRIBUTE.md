# Contributor Guidelines

Here are some guidelines on how one can contribute to this project. Please feel free to ask more questions to clarify any details.

# Git Flow

## Branching

Our Git flow is a simplified Git-Flow. Much like Git-Flow, we take advantage of a main branch, a development branch, and feature branches.

### The main Branch 
This branch remains readily deployable at all times. It has no end to its lifespan and only heavily tested code (or no code at all) is allowed in this exclusive branch. Any pull request to the main branch should be considered a new release.

### The development Branch 
This branch is where all ongoing work is done. It runs parallel to main and incorporates all bug fixes and features planned for specific release. When all planned features are implemented and the head of the development branch is tested and meets our coding requirements (to be discussed later) we are ready to create a PR to main.

### feature Branches 
feature branches branch off of development and must be merged back into development. A feature branch adds end-user functionality to the application. Each feature is described and discussed through the DLTS project tracking system (currently JIRA).  When working on a feature branch, it is important to only make changes that are relevant to the feature you are currently working on. Thus the lifespan of the feature branch is limited to the development of that feature. As a convention, we prefix feature branch names with the Jira ticket number.

### chore Branches 
chore branches branch off of development and must be merged back into development. A chore branch does not add end-user functionality but is used for housekeeping tasks (e.g., updating a configuration file). When working on a chore branch, it is important to only make changes that are relevant to the chore you are currently working on. Thus the lifespan of the chore branch is limited to the completion of the chore. As a convention, we prefix chore branch names with chore/ (e.g., chore/update-database-config).

### Hotfix Branches 
Hotfix branches are necessary in case we need an immediate fix in the current production system. Hotfix branches branch off of the main branch and must be merged back to development and main branches through pull request.

## Committing
Commit often! Your commits tell the story of your project. We expect to have well written commit messages. Your commits should reflect what changes you made to the code base and should be coherent, cohesive, concise, and isolated. This way it becomes easy to track what change affects the product as a whole.
That being said, the message itself should be written in the imperative. The end result will have your Git Commit history looking like a recipe for success!
For example, when I finish this document and submit it, my Git Commit will probably be:
Add CONTRIBUTING.md

Add documentation for expectations on contributing.

## Pull Requests
When you're confident in your code, you're going to want to send in a pull request. Your commit history will be able to tell the code maintainer what you've changed and how it will affect the codebase. It may be a good idea to summarize what you have done in the pull request message and how it will affect the codebase. All pull requests require at least one review and approval from other project developers.
If the merging of your code requires additional operations other than a simple merge and deploy, you should include the additional steps in your pull request. For example, if you're adding a new collection, you would add "Requires collection data load" to the PR.
Sometimes the development branch will be updated while you have an open PR. When this happens, your branch might become stale, meaning that your branch can no longer be merged into development without a conflict. When this happens you should:
rebase your branch onto the latest version of development, resolving any merge conflicts
delete your stale branch on GitHub, which will automatically close the PR for your stale branch
push your newly rebased branch up to GitHub
create a new PR that contains a reference to the old PR
For example, let's say you have submitted a PR (#432) for branch feature/gizmo, but this branch has gone stale and cannot be merged. You should do the following:
step
comment
$ git pull origin development
gets the latest version of development
$ git checkout feature/gizmo
checks out your branch locally
$ git rebase development
replays your changes on top of the latest development branch
resolve any conflicts

$ git push origin :feature/gizmo
deletes your stale branch on GitHub and automatically closes PR #432 (Note the : before the branch name)
$ git push origin feature/gizmo
pushes the merge-able version of your branch up to GitHub

Now you can create a new PR for feature/gizmo in GitHub, include a reference to the old PR (#432) in your new PR


### Code Review
After sending your pull request, your code will get reviewed to make sure merging it won't break the branch it's merging into. This is a good time to ask any questions or concerns you have. Code reviews also help get a fresh set of eyes to look at your code, and if those eyes are also working on the project, it lets them get familiar with the new code base.
#Testing
We expect developers to use test driven development (i.e., create a test for a requested feature before it is implemented). We have GitHub actions configured to run the project test suite for each pull request submitted to the development branch and for each commit to the main branch.  Project test suite now includes tests written using pytest library and fixtures provided in flask-pytest and pytest-invenio modules. Those technologies have some limitations so we are currently considering integration of the nightwatch testing tool to the project.


# Issue Tracking
If you find any issues in the code base, feel free to open up an issue using GitHub's issues feature. You can assign issues to users, label them, and set them to milestones.
This is also true if you find issues with the general User Experience or anything else.  


# Comments
It's a good idea to include an inline comment explaining how your code works. Keep in mind that if your comments are too complicated, the problem might be with the code. If you copy code, provide links to the original source of copied code. Include links to external references where they will be most helpful. Add comments when fixing bugs and/or adding features (include reference to the Jira ticket). Use comments to mark incomplete implementations. For example, you can use #TODO or #IMPORTANT.

 
# Best Practices
[back to top](#contributor guidelines)

For best practices, give every class, method, and variable a clear, semantic name, along with comments explaining the code's purpose. Try to avoid cluttered comments and large methods. The human eye is attracted to empty space, so breaking up large blocks of code to succinct blocks with small comments is highly visible and easier to follow.


# More Resources
Blog post on our workflows
Some more info on pull requests, and why code reviews are important.
5 useful tips on how to write a better git commit message
A Note About Git Commit Messages.
