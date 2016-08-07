from cStringIO import StringIO

from ..helpers.s3 import S3IO
from .base import BaseStorage


class S3Storage(S3IO, BaseStorage):

    def save(self, path, img, save_options):
        name = self.get_name(path)
        key = self.bucket.new_key(name)
        key.set_acl(self.config.ACL)
        f = StringIO()
        img.save(f, format=img.format, **save_options)
        key.set_contents_from_file(f)
