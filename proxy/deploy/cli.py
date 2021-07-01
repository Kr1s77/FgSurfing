import os
import tarfile
import zipfile
import argparse
from adb import Device

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


def push_to_mobile(filepath: str, remote_path: str, device: Device) -> str:
    device.adb.push(
        filepath=filepath,
        remote_path=remote_path
    )
    return remote_path


def decompress_mobile_file(remote_path: str, remote_file: str, device: Device) -> str:
    device.adb.decompress(
        remote_path=remote_path,
        remote_file=remote_file,
    )
    return remote_file


def rm_and_mk_dir(remote_path: str,  device: Device) -> str:
    device.adb.delete_and_create_dir(
        remote_path=remote_path
    )
    return remote_path


def deploy_to_remote(device: Device):
    output_filename = os.path.basename(proxy_dir) + '.tar.gz'
    make_gz(output_filename, proxy_dir)

    filepath = os.path.join(proxy_dir, output_filename)
    mobile_file_path = push_to_mobile(
        filepath=filepath,
        remote_path='/data/local/tmp/',
        device=device
    )
    # print(f'*{output_filename}* was pushed to mobile *{mobile_file_path}*')
    mobile_compress_file = os.path.join(mobile_file_path, output_filename)
    mobile_script_file = os.path.join(mobile_file_path, os.path.basename(proxy_dir))

    # decompress script file
    # rm and mk dir
    rm_and_mk_dir(remote_path=mobile_script_file, device=device)

    decompress_mobile_file(
        remote_path=mobile_compress_file,
        remote_file=mobile_file_path,
        device=device
    )

    # clean local compress file
    os.popen(f'rm -rf {filepath}')

    # create remote server


