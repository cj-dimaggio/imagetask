import os

from io import BytesIO

from imagetask.config import ConfigDef, Configurable


class S3IO(Configurable):
    config = ConfigDef({
        'KEY': ConfigDef.RequiredField,
        'SECRET': ConfigDef.RequiredField,
        'BUCKET': ConfigDef.RequiredField,
        'PREFIX': '',
        'ACL': 'private'
    })

    def __init__(self):
        self._bucket = None
        self._connection = None

    def get_name(self, name):
        return os.path.join(self.config.PREFIX, name).encode('utf-8')

    def get(self, path, mode='rb'):
        name = self.get_name(path)
        key = self.bucket.get_key(name)
        f = BytesIO()
        key.get_contents_to_file(f)
        f.seek(0)
        return f

    def exists(self, name):
        name = self.get_name(name)
        return bool(self.bucket.get_key(name))

    def _get_or_create_bucket(self, name):
        try:
            return self.connection.get_bucket(name)
        except Exception as e:
            raise Exception(
                "Bucket %s does not exist, or is inaccessible: %s." % (name, e))

    @property
    def connection(self):
        import boto
        if self._connection is None:
            self._connection = boto.connect_s3(self.config.KEY,
                                               self.config.SECRET)

        return self._connection

    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = self._get_or_create_bucket(self.config.BUCKET)
        return self._bucket
