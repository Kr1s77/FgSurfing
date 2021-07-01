import os
import logging
import tarfile
import zipfile
import argparse
from api import configure_logging

log = logging.getLogger(__name__)
configure_logging(logging.INFO)

# Default dir path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
proxy_dir = os.path.join(current_dir, 'proxy')


def make_gz(output_filename: str, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def make_zip(output_filename: str, source_dir):
    zip_file = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, _, filenames in os.walk(source_dir):
        for filename in filenames:
            path_file = os.path.join(parent, filename)
            name = path_file[pre_len:].strip(os.path.sep)  # 相对路径
            zip_file.write(path_file, name)
    zip_file.close()


def push_to_mobile(filepath: str) -> str:
    return 'data/local/tmp/'


def decompress_mobile_file(filepath: str) -> str:
    pass


def create(compress: str):
    if compress == 'zip':
        output_filename = os.path.basename(proxy_dir) + '.zip'
        make_gz(output_filename, proxy_dir)
    elif compress == 'gz':
        output_filename = os.path.basename(proxy_dir) + '.tar.gz'
        make_gz(output_filename, proxy_dir)
    else:
        output_filename = None
        log.error('Compress must be "zip" or "gz"')
        exit(1)

    filepath = os.path.join(os.path.join(proxy_dir, 'deploy'), output_filename)
    mobile_file_path = push_to_mobile(filepath=filepath)
    log.info(f'*{output_filename}* was pushed to mobile *{mobile_file_path}*')


if __name__ == '__main__':
    create('gz')