#!/usr/bin/env python

"""
Builds a zip package for multi-container elastic beanstalk environments
"""

import logging
import os
import subprocess
import ebcli.core.fileoperations as fileoperations

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if not os.path.exists('.elasticbeanstalk'):
    os.mkdir('.elasticbeanstalk')

sha = subprocess.check_output(['git', 'rev-parse', '--short=7', 'HEAD']).decode('utf-8').rstrip()
print('::set-env name=CONTAINER_SHA::{}'.format(sha))

file_name = 'sha-' + sha + '.zip'
file_path = fileoperations.get_zip_location(file_name)

logging.info('Packaging application to %s', file_path)
ignore_files = fileoperations.get_ebignore_list()
fileoperations.io.log_info = lambda message: logging.debug(message)
fileoperations.zip_up_project(file_path, ignore_list=ignore_files)