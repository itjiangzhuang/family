__author__ = 'jiangzhuang'

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app

print "************* CURRENT CONFIG MODE: ", os.getenv('YUNDONG99_APP_CONFIG_MODE')
mode = os.getenv('YUNDONG99_APP_CONFIG_MODE') or 'default'
if mode:
    mode = mode.lower()

app = create_app(mode)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
