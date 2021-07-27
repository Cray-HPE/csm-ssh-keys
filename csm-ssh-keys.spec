# Copyright 2020-2021 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# (MIT License)
Name: csm-ssh-keys
License: MIT
Summary: Ansible modules and roles for use with CSM SSH Key Distribution
Group: System/Management
Version: %(cat .version)
Release: %(echo ${BUILD_METADATA})
Source: %{name}-%{version}.tar.bz2
Vendor: Hewlett Packard Enterprise Development LP

%define ansible_base_dir     /opt/cray/ansible/
%define ansible_playbook_dir %{ansible_base_dir}playbooks/
%define ansible_modules_dir  %{ansible_base_dir}modules/
%define ansible_roles_dir    %{ansible_base_dir}roles/
%define ansible_requires_dir %{ansible_base_dir}requirements/

%package roles
Group: System/Management
Summary: Provides roles for interacting with Cray System Management SSH Key Deployment

%description
Provides ansible content necessary for interacting with Cray System Management SSH Key Deployment

%description roles
Provides client side roles necessary for bootstrapping interactive SSH trust
between environments

%prep
%setup -q

%build

%install
# Modules
install -m 755 -d %{buildroot}%{ansible_modules_dir}
install -D -m 644 ansible/modules/csm_read_configmap.py %{buildroot}%{ansible_modules_dir}/csm_read_configmap.py
install -D -m 644 ansible/modules/csm_read_secret.py   %{buildroot}%{ansible_modules_dir}/csm_read_secret.py


# Roles
install -m 755 -d %{buildroot}%{ansible_roles_dir}
cp -r ansible/roles/* %{buildroot}%{ansible_roles_dir}/.

# Requirements
install -m 755 -d   %{buildroot}%{ansible_requires_dir}/.
cp module_requirements.txt %{buildroot}%{ansible_requires_dir}/csm_ssh_keys.txt

%files
%defattr(755, root, root)
%dir %{ansible_modules_dir}
%{ansible_modules_dir}/csm_read_configmap.py
%{ansible_modules_dir}/csm_read_secret.py

%dir %{ansible_requires_dir}
%{ansible_requires_dir}/csm_ssh_keys.txt

%files roles
%defattr(755, root, root)
%dir %{ansible_roles_dir}
%{ansible_roles_dir}/trust-csm-ssh-keys/*
%{ansible_roles_dir}/passwordless-ssh/*
