from pathlib import Path
import re
import subprocess
from typing import Dict
import yaml


def get_conda_packages(conda_list_output: str) -> Dict[str, Dict[str, str]]:
    """Extracts Conda packages from the output of 'conda list --explicit'"""
    
    # TODO: Better parsing of conda channel vis-a-vis extension (e.g. .conda)
    # conda_regex = r"https://conda.anaconda.org/(.*?)/(osx-64|noarch)/(.*?)-([0-9\.]*)([_\-\d\w]*).conda"
    
    # Is this better?
    conda_regex = r"https://conda.anaconda.org/(.*?)/(osx-64|noarch)/(.*?)-([0-9\.]*)([_\-\d\w]*)(.conda)?"
    conda_packages = {}

    for line in conda_list_output.split('\n'):
        if not line.startswith('https://'):
            continue
        match = re.match(conda_regex, line)
        if match:
            channel, _, package, version, _, extension = match.groups()
            if (channel == 'conda-forge' and extension) or channel != 'conda-forge':
                conda_packages[package] = {'channel': channel, 'version': version}
    return conda_packages

def get_pip_packages(pip_freeze_output: str, conda_packages: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    """Extracts pip packages from the output of 'pip freeze'"""
    pip_packages = {}

    for line in pip_freeze_output.split('\n'):
        if line and not '@' in line:
            package, version = line.split('==')
            if package not in conda_packages:
                try:
                    pip_packages[package] = version.split('.')[:2]  # MAJOR.MINOR
                except IndexError:
                    pip_packages[package] = None
                except ValueError:
                    pip_packages[package] = None
    return pip_packages

def env_to_yaml(env: str, output_dir: str = Path.cwd(), overwrite: bool = False):
    """Generates a Conda environment YAML file from the given environment
    
    # Call the function with the environment name
    env_to_yaml('my-env')
    """
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True)
    
    if not overwrite and (Path(output_dir) / f'{env}.yml').exists():
        raise FileExistsError(f'File {Path(output_dir) / f"{env}.yml"} already exists. Set overwrite to True to overwrite the file.')

    # Get Conda packages
    conda_list_output = subprocess.check_output(["conda", "list", "--explicit", "-n", env], universal_newlines=True)
    conda_packages = get_conda_packages(conda_list_output)

    # Get pip packages
    pip_freeze_output = subprocess.check_output(["pip", "freeze"], universal_newlines=True)
    pip_packages = get_pip_packages(pip_freeze_output, conda_packages)

    # Prepare data for the YAML file
    data = {
        'name': env,
        'channels': ['conda-forge'],
        'dependencies': ['pip']
    }

    # Fill in channels and dependencies for Conda packages
    for package, details in conda_packages.items():
        if details['channel'] not in data['channels']:
            data['channels'].append(details['channel'])
        try:
            major_version, minor_version = details['version'].split('.')[:2]
            data['dependencies'].append(f"{package}={major_version}.{minor_version}")
        except IndexError:
            data['dependencies'].append(package)
        except ValueError:
            data['dependencies'].append(package)

    # Fill in dependencies for pip packages
    if pip_packages:
        data['dependencies'].append({'pip': [f"{package}=={'.'.join(version)}" if version else package for package, version in pip_packages.items()]})

    # Write the data to the YAML file
    with open(Path(output_dir) / f'{env}.yml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False)