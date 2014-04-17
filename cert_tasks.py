from boto.s3.connection import S3Connection
from boto.s3.key import Key
from invoke import task, run
import hashlib
import requests

@task
def generate(filename=''):
    filename = filename if filename else 'cacerts.pem'
    run("curl https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt -o certdata.txt")
    run("extract-nss-root-certs > '%s'" % filename)

@task
def diff(gen=False, filename=''):
    filename = filename if filename else 'cacerts.pem'

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

@task
def upload(filename=''):
    filename = filename if filename else 'cacerts.pem'

    # This method requires the environment variables AWS_ACCESS_KEY_ID and
    # AWS_SECRET_ACCESS_KEY to be set appropriately.
    conn = S3Connection()
    b = conn.get_bucket('certifi-bundles')
    k = Key(b)

    with open('cacerts.pem', 'rb') as f:
        k.key = hashlib.sha1(f.read()).hexdigest() + '.pem'

    k.set_contents_from_filename('cacerts.pem')

    k = Key(b)
    k.key = 'latest.pem'
    k.set_contents_from_filename('cacerts.pem')
