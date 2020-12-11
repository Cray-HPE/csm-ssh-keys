# setup.py for cfsssh-setup
# Copyright 2020 Hewlett Packard Enterprise Development LP
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(".version", "r") as fh:
    version_str = fh.read()

package_dir = {'csmsshkeys': 'src/csmsshkeys',}

setuptools.setup(
    name="csmsshkeys",
    version=version_str,
    author="HPE Development LP",
    author_email="sps@cray.com",
    description="CSM SSH Key Initialization Deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stash.us.cray.com/projects/SCMS/repos/csm-ssh-keys/browse",
    package_dir = package_dir,
    packages = list(package_dir.keys()),
    keywords="vault ssh kubernetes csm",
    classifiers=(
        "Programming Language :: Python :: 3.8",
        "License :: Other/Proprietary License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ),
)
