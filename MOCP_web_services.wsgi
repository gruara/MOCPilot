#!/usr/bin/python3

import logging
import sys
#logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/MOCPilot')
from MOCP_web_services import app as application
