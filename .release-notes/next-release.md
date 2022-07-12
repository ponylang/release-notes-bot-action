## Update to work with newer versions of git

Newer versions of git have added a check to see if the user running a command is the same as the user who owns the repository. If they don't match, the command fails. Adding the repository directory to a "safe list" addresses the issue.

We've updated accordingly.

