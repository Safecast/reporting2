import json
import logging
import os
import re
from urllib.parse import urlparse

import boto3
import ebcli.core.fileoperations as fileoperations

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def replace_docker_images():
    image_replacements = json.loads(os.environ['INPUT_CONTAINER_IMAGES'])

    with open('Dockerrun.aws.json') as f:
        data = json.load(f)
        for container_definition in data['containerDefinitions']:
            name = container_definition['name']
            if name in image_replacements.keys():
                container_definition['image'] = image_replacements[name]

    with open('Dockerrun.aws.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def add_authentication_key(bucket):
    if 'INPUT_AUTHENTICATION_KEY' not in os.environ:
        return

    with open('Dockerrun.aws.json') as f:
        data = json.load(f)
        data['authentication'] = {
            'bucket': bucket,
            'key': os.environ['INPUT_AUTHENTICATION_KEY']
        }

    with open('Dockerrun.aws.json', 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def build_bundle(version_label):
    if not os.path.exists('.elasticbeanstalk'):
        os.mkdir('.elasticbeanstalk')
    file_path = fileoperations.get_zip_location('{}.zip'.format(version_label))
    logging.info('Packaging application to %s', file_path)
    ignore_files = fileoperations.get_ebignore_list()
    fileoperations.io.log_info = lambda message: logging.debug(message)
    fileoperations.zip_up_project(file_path, ignore_list=ignore_files)
    return '.elasticbeanstalk/app_versions/{}.zip'.format(version_label)


def build_version_label():
    app = os.environ['INPUT_APP']
    ref = os.environ['GITHUB_REF']

    ref_no_prefix = re.sub('^refs/(heads/)?', '', ref)
    ref_no_suffix = re.sub('/head$', '', ref_no_prefix)
    ref_special_as_underscore = re.sub('[-/]', '_', ref_no_suffix)

    clean_branch_name = ref_special_as_underscore

    build_number = os.environ['GITHUB_RUN_ID']
    git_sha = os.environ['GITHUB_SHA']
    return "{}-{}-{}-{}".format(app, clean_branch_name, build_number, git_sha)


def build_description():
    hostname = urlparse(os.environ['GITHUB_SERVER_URL']).netloc
    repository = os.environ['GITHUB_REPOSITORY']
    run_id = os.environ['GITHUB_RUN_ID']
    return '{}/{}/actions/runs/{}'.format(hostname, repository, run_id)


def upload_bundle(file_name, bucket, app):
    key = '{}/{}'.format(app, os.path.basename(file_name))
    # noinspection PyUnresolvedReferences
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, key)
    return key


def create_app_version(app, version_label, bucket, key):
    # noinspection PyUnresolvedReferences
    elasticbeanstalk = boto3.client('elasticbeanstalk')
    elasticbeanstalk.create_application_version(
        ApplicationName=app,
        VersionLabel=version_label,
        Description=build_description(),
        SourceBundle={
            'S3Bucket': bucket,
            'S3Key': key
        }
    )


def main():
    app = os.environ['INPUT_APP']
    bucket = os.environ['INPUT_S3_BUCKET']

    replace_docker_images()
    add_authentication_key(bucket)
    version_label = build_version_label()
    file_name = build_bundle(version_label)

    key = upload_bundle(file_name, bucket, app)
    create_app_version(app, version_label, bucket, key)


if __name__ == "__main__":
    main()
