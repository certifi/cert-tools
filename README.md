# Certifi cert-tools

This repository contains the tooling used to generate the certifi certificate
bundle. Some of these tools are useful generally: others are only useful in the
context of the certifi project.

The following tools are included:

- `update-certify.py`: A script that automatically updates the official certifi
  releases.

## The Tools

### $ update-certify.py

This script is used to update the `certifi` libraries in their various languages
to the newest certificates. It is run in response to a change in the certificate
bundle used by `certifi`.

This tool functions by checking out the GitHub repositories containing the
`certifi` libraries and updating them according to their specific
[invoke](http://invoke.readthedocs.org/en/latest/) scripts. This causes these
libraries to push new releases to their relevant package managers.

For obvious reasons, this can only be run by people with access to the `certifi`
repositories.

### $ cert_tasks.py

This provides a series of tasks for use with
[invoke](http://invoke.readthedocs.org/en/latest/).  It requires that
`extract-nss-root-certs` is somewhere on your `$PATH`. You can run three
commands:

1. `invoke -c cert_tasks generate`. This task generates a `cacerts.pem` file in
   the local directory. This takes a single argument, `filename`, that can be
   used to set a different filename, eg. `--filename="test.pem"`
2. `invoke -c cert_tasks diff`. This task diffs `cacerts.pem` against the latest
   uploaded `.pem` file, and prints whether the two are different. This takes
   two optional arguments: `--filename`, which works as above; and `--gen`,
   which runs the generate step before diffing.
3. `invoke -c cert_tasks upload`. This task uploads the new `.pem` file to your
   S3 bucket.

### $ extract-nss-root-certs

This tool converts the Mozilla certificate file into a *.pem file that excludes
all untrusted certificates. The tool is not included in this repository, as it's
written in Go: it can be found
[here](https://github.com/certifi/extract-nss-root-certs). Rather than building
this code yourself, you can download a binary from
[here](https://github.com/certifi/extract-nss-root-certs/releases). This avoids
the need for a Go compiler.
