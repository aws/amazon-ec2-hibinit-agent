#
# spec file for ec2-hibernate-linux-agent
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%{?python_enable_dependency_generator}

%global project         amazon-ec2-hibinit-agent

# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

Name:           ec2-hibernate-linux-agent
Version:        1.0.4
Release:        1%{?dist}
Summary:        Hibernating Agent for Linux on Amazon EC2

Group:          System/Management
License:        MIT
URL:            https://github.com/aws/%{project}
Source0:        https://github.com/aws/%{project}/archive/v%{version}/ec2-hibinit-agent-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: systemd-rpm-macros
BuildRequires: python3-devel
BuildRequires: pkgconfig(systemd)
BuildRequires: python-rpm-generators
BuildRequires: tuned
BuildRequires: bzip2

Requires: acpid 
Requires: grubby 
Requires: systemd 
Requires: tuned

%description
Hibernating Agent for Linux on Amazon EC2

This agent does several things:

1. Upon startup it checks for sufficient swap space to allow hibernate
   and fails if it's present but there's not enough of it.
2. If there's no swap space, it creates it and launches a background
   thread to touch all of its blocks to make sure that EBS volumes
   are pre-warmed.
3. It updates the offset of the swap file in the kernel using
   SNAPSHOT_SET_SWAP_AREA ioctl.
4. It daemonizes and starts a polling thread to listen for instance
   termination notifications.

%prep
%autosetup -n %{project}-%{version}
 
%build
%py3_build

%install
%py3_install --root %{buildroot}

mkdir -p %{buildroot}%{python3_sitelib}
mkdir -p "%{buildroot}%{_unitdir}"
mkdir -p %{buildroot}%{_sysconfdir}/acpi/events 
mkdir -p %{buildroot}%{_sharedstatedir}/hibinit-agent
mkdir -p %{buildroot}%{_sysconfdir}/acpi/actions
mkdir -p %{buildroot}%{_sbindir}

install -p -m 644 "%{_builddir}/%{project}-%{version}/hibinit-agent.service" %{buildroot}%{_unitdir}
install -p -m 644 "%{_builddir}/%{project}-%{version}/acpid.sleep.conf" %{buildroot}%{_sysconfdir}/acpi/events/sleepconf

mkdir -p %{buildroot}%{_prefix}/lib/systemd/logind.conf.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-sleep

install -p -m 644 "%{_builddir}/%{project}-%{version}/etc/hibinit-config.cfg" %{buildroot}/%{_sysconfdir}/hibinit-config.cfg
install -p -m 644 "%{_builddir}/%{project}-%{version}/packaging/rhel/00-hibinit-agent.conf" %{buildroot}%{_prefix}/lib/systemd/logind.conf.d/00-hibinit-agent.conf
install -p -m 755 "%{_builddir}/%{project}-%{version}/packaging/rhel/acpid.sleep.sh" %{buildroot}%{_sysconfdir}/acpi/actions/sleep.sh
install -p -m 755 "%{_builddir}/%{project}-%{version}/packaging/rhel/sleep-handler.sh" %{buildroot}%{_prefix}/lib/systemd/system-sleep/sleep-handler.sh

#Disable transparent huge page
mkdir -p  %{buildroot}%{_sysconfdir}/tuned/nothp_profile
install -p -m 644 "%{_builddir}/%{project}-%{version}/packaging/rhel/tuned.conf" %{buildroot}%{_sysconfdir}/tuned/nothp_profile/tuned.conf

ln -sf %{_sbindir}/service %{buildroot}%{_sbindir}/rchibinit-agent

%files
%doc README.md
%license LICENSE.txt
%config(noreplace) %{_sysconfdir}/hibinit-config.cfg
%{_unitdir}/hibinit-agent.service
%{_bindir}/hibinit-agent
%{_sbindir}/rchibinit-agent
%config(noreplace) %{_sysconfdir}/acpi/events/sleepconf
%config(noreplace) %{_sysconfdir}/acpi/actions/sleep.sh
%{python3_sitelib}/ec2_hibinit_agent-*.egg-info/
%dir %{_sharedstatedir}/hibinit-agent
%ghost %attr(0600,root,root) %{_sharedstatedir}/hibinit-agent/hibernation-enabled

%dir %{_prefix}/lib/systemd/logind.conf.d
%dir %{_prefix}/lib/systemd/system-sleep
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions


%dir %{_sysconfdir}/tuned/nothp_profile
%config(noreplace) %{_sysconfdir}/tuned/nothp_profile/tuned.conf

%{_prefix}/lib/systemd/system-sleep/sleep-handler.sh
%{_prefix}/lib/systemd/logind.conf.d/00-hibinit-agent.conf


%pre
%service_add_pre hibinit-agent.service

%post
%service_add_post hibinit-agent.service

#
# Disable THP by switching to nothp_profile profile
#
tuned-adm profile nothp_profile


%preun
%service_del_preun hibinit-agent.service


%postun
%systemd_postun_with_restart hibinit-agent.service


%changelog
