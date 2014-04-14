# Certifi cert-tools

This repository contains the tooling used to generate the certifi certificate
bundle. Some of these tools are useful generally: others are only useful in the
context of the certifi project.

The following tools are included:

- `update-certify.py`: A script that automatically updates the official certifi
  releases.

## The Tools

### update-certify.py

This script is used to update the `certifi` libraries in their various languages
to the newest certificates. It is run in response to a change in the certificate
bundle used by `certifi`.

This tool functions by checking out the GitHub repositories containing the
`certifi` libraries and updating them according to their specific
[invoke](http://invoke.readthedocs.org/en/latest/) scripts. This causes these
libraries to push new releases to their relevant package managers.

For obvious reasons, this can only be run by people with access to the `certifi`
repositories.
