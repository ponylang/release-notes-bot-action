## Update to work with newer versions of git

Newer versions of git have added a check to see if the user running a command is the same as the user who owns the repository. If they don't match, the command fails. Adding the repository directory to a "safe list" addresses the issue.

We've updated accordingly.

## Updated base image

We've updated our base image from Alpine 3.12 to 3.16. Alpine 3.12 is no longer supported.

