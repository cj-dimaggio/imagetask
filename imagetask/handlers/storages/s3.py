from io import BytesIO

from ..helpers.s3 import S3IO
from .base import BaseStorage


class S3Storage(S3IO, BaseStorage):

    def save(self, path, f):
        name = self.get_name(path)
        key = self.bucket.new_key(name)
        f.seek(0)
        key.set_contents_from_file(f)
        key.set_acl(self.config.ACL)
        f.seek(0)
        return f
