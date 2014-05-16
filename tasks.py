
import os
import hashlib

import requests
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from invoke import task, run

MOZILLA_BUNDLE = 'https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt'

@task
def generate(filename='cacerts.pem'):

    run('curl {} -o certdata.txt'.format(MOZILLA_BUNDLE))
    run("extract-nss-root-certs > '%s'" % filename)

@task
def diff(gen=False, filename='cacerts.pem'):

    if gen:
        generate(filename)

    r = requests.get('http://certifi-bundles.s3.amazonaws.com/latest.pem')
    r.raise_for_status()

    # Compare the hashes of the two files.
    old = hashlib.sha1(r.content).hexdigest()
    new = hashlib.sha1(open(filename, 'rb').read()).hexdigest()

    if old == new:
        print 'No change.'
    else:
        print 'Certs are different, you should upload.'
        exit(1)
        # TODO: --upload  e.g. && upload()

@task
def upload(filename='cacerts.pem'):

    # This method requires the environment variables to be set appropriately:
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_BUCKET_NAME.

    BUCKET_NAME = os.environ['AWS_BUCKET_NAME']

    s3 = S3Connection()
    bucket = s3.get_bucket(BUCKET_NAME)


    # Deploy the CA Bundle to production.

    k = Key(bucket)

    with open('cacerts.pem', 'rb') as f:
        k.key = hashlib.sha1(f.read()).hexdigest() + '.pem'

    k.set_contents_from_filename(filename)


    # TODO: setup object redirect.
    k = Key(bucket)
    k.key = 'latest.pem'
    k.set_contents_from_filename(filename)
