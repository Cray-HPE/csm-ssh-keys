# Copyright 2020 Hewlett Packard Enterprise Development LP
Name: csm-ssh-keys
License: Cray Software License Agreement
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

%clean
rm -f  %{buildroot}%{modules}/*

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
