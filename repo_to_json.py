#!/usr/bin/env python
from cd import cd
import git_manager as gm
import os
import os.path
import subprocess
import errno


def get_filelist(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_list.append(root + '/' + file)

    return file_list


def is_path_exist(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def process_local_repo(location, output_dir, repo_name):
    with cd(location):
        is_path_exist(output_dir)

        output_file_code = output_dir + "/" + repo_name.replace('/', '_') + "_code.txt"
        file_list = get_filelist(location)
        with open(output_file_code, 'w+') as out:
            for i, file in enumerate(file_list):
                with open(file, 'r') as input_file:
                    while True:
                        data = input_file.read(100000)
                        if data == '':
                            break
                        out.write(data)
                if i % 500 == 0 and i != 0:
                    print(f'Copied {i} out of {len(file_list)} files')


def get_local_repo_name(location):
    with cd(location):
        command = [
            "git",
            "rev-parse",
            "--show-toplevel",
        ]
        repo_name = subprocess.check_output(command)
        base = os.path.basename(repo_name).strip()
        return base


if __name__ == "__main__":

    import argparse
    # Set up command line flag handling
    parser = argparse.ArgumentParser(
        description="Clone and parse a git repository",
    )
    parser.add_argument(
        'repo_location',
        type=str,
        help="the location of the repository"
    )
    parser.add_argument(
        'output_directory',
        type=str,
        action="store",
        help="the directory to save the output JSON files",
    )
    parser.add_argument(
        '-n',
        '--repo-name',
        type=str,
        action="store",
        help="override the default repository name to save to the JSON file"
    )

    args = parser.parse_args()

    repo_name = str(args.repo_name)

    with gm.Repository(args.repo_location) as repo:
        if not repo_name:
            repo_name = str(get_local_repo_name(repo.local_location))
        process_local_repo(
            repo.local_location,
            args.output_directory,
            repo_name
        )
