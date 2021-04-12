%{?python_enable_dependency_generator}

%global project         amazon-ec2-hibinit-agent

# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

Name:           ec2-hibinit-agent
Version:        1.0.4
Release:        1%{?dist}
Summary:        Hibernation setup utility for Amazon EC2

License:        Apache-2.0
Group:          System/Boot
URL:            https://github.com/aws/amazon-%{name}
Source0:        https://github.com/aws/%{project}/archive/v%{version}/%{name}-%{version}.tar.gz

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
An EC2 agent that creates a setup for instance hibernation

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

* Mon Apr 12 2021 Mohamed Aboubakr <mabouba@amazon.com> - 1.0.4-1
- Support Open Use by creating new spec file and removing selinux modules.
- Added systemd as a required.

* Thu Jan 14 2021 Mohamed Aboubakr <mabouba@amazon.com> - 1.0.4-1
- Call grub2-mkconfig in hibernate agent before calling grubby

* Tue Nov 03 2020 Mohamed Aboubakr <mabouba@amazon.com> - 1.0.3-3
- Moving selinux folder in packaging directory.
- Use make file to generate .pp.bz2 file

* Fri Oct 02 2020 David Duncan <davdunc@amazon.com> - 1.0.3-2
- Modify Spec for build requirements

* Thu Aug 13 2020 Mohamed Aboubakr <mabouba@amazon.com> - 1.0.3-1
- Support Redhat and Fedora by adding sepolicy
- Ignore handle hibernation in systemd configuration

* Fri Jan 24 2020 Frederick Lefebvre <fredlef@amazon.com> - 1.0.1-2
- Restart the hibinit-agent service on upgrade

* Thu Jan 23 2020 Frederick Lefebvre <fredlef@amazon.com> - 1.0.1-1
- Added IMDSv2 support
- Renamed spec file to match the actual package name

* Fri Jun 14 2019 Anchal Agarwal <anchalag@amazon.com> - 1.0.0-4
- Added hibernation re-try logic in case of hibernation failure

* Wed Nov 07 2018 Matt Dees <mattdees@amazon.com> - 1.0.0-2
- Clean up hibernation configured check

* Wed Oct 31 2018 Anchal Agarwal <anchalag@amazon.com> - 1.0.0-1
- Initial build
