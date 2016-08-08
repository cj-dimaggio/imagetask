import os
import yaml
import argparse
from flask import Flask
from imagetask.server.flask_plugin import register_imagetask

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='YAML Configuration file',
                    required=True)
parser.add_argument('--host', help='Host for flask application')
parser.add_argument('--port', help='Port for flask application')
parser.add_argument('--debug', help='Debug flask application',
                    action='store_true')
args = parser.parse_args()

app = Flask(__name__)

if not os.path.exists(args.config):
    raise Exception('File %s does not exists' % args.config)
config = yaml.load(open(args.config, 'r'))

register_imagetask(app, config)

if __name__ == '__main__':
    app.run(host=args.host, port=args.port, debug=args.debug)
