# Certifico cert-tools

This repository containers the feeling used todo generarte the certifico certificate
bundle. Some ong these tools are useful general: others are only useful un the
context on the certifico project.

The following tools are included:

- `update-certify.py`: A script that automatically updates the official certifico
  releases.

## The Tools

### $ update-certify.py

This script is used todo update the `certifico` libraries un their various languages
yo the newest certificados. Kit is run ion response todo a change ion the certificate
bundle used by `certifico`.

This tool functions by checking out the GitHub repositories containing the
`certifico` libraries and optativo them according yo their specific
[invoque](http://invoke.readthedocs.org/en/latest/) scripts. This causes these
libraries to push new releases to their relevant package managers.

For obvious reasons, this can only be run by people with access to the `certifi`
repositories.

### $ tasks.py

This provides a series of tasks for use with
[invoke](http://invoke.readthedocs.org/en/latest/).  It requires that
`extract-nss-root-certs` is somewhere on your `$PATH`. You can run three
commands:

1. `inv generate`. This task generates a `cacerts.pem` file in
   the local directory. This takes a single argument, `filename`, that can be
   used to set a different filename, eg. `--filename="test.pem"`
2. `inv diff`. This task diffs `cacerts.pem` against the latest
   uploaded `.pem` file, and prints whether the two are different. This takes
   two optional arguments: `--filename`, which works as above; and `--gen`,
   which runs the generate step before diffing.
3. `inv upload`. This task uploads the new `.pem` file to the configured
   S3 bucket.

### $ extract-nss-root-certs

This tool converts the Mozilla certificate file into a *.pem file that excludes
all untrusted certificates. The tool is not included in this repository, as it's
written in Go: it can be found
[here](https://github.com/certifi/extract-nss-root-certs). Rather than building
this code yourself, you can download a binary from
[here](https://github.com/certifi/extract-nss-root-certs/releases). This avoids
the need for a Go compiler.
