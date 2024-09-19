Name:           ec2-hibinit-agent
Version:        1.0.10
Release:        1%{?dist}
Summary:        Hibernation setup utility for AWS EC2

Group:          System Environment/Daemons
License:        Apache 2.0
Source0:        ec2-hibinit-agent-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  systemd
%{?systemd_requires}

Requires: acpid
Requires: grubby
Requires: pm-utils
%description
An EC2 agent that creates a setup for instance hibernation

%prep
%setup -q -n ec2-hibinit-agent-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --prefix=usr -O1 --skip-build --root $RPM_BUILD_ROOT
mkdir -p "%{buildroot}%{_unitdir}"
mkdir -p %{buildroot}%{_sysconfdir}/acpi/events
mkdir -p %{buildroot}%{_sysconfdir}/acpi/actions
mkdir -p %{buildroot}%{_localstatedir}/lib/hibinit-agent
install -p -m 644 "%{_builddir}/%{name}-%{version}/hibinit-agent.service" %{buildroot}%{_unitdir}
install -p -m 644 "%{_builddir}/%{name}-%{version}/acpid.sleep.conf" %{buildroot}%{_sysconfdir}/acpi/events/sleepconf
install -p -m 755 "%{_builddir}/%{name}-%{version}/acpid.sleep.sh" %{buildroot}%{_sysconfdir}/acpi/actions/sleep.sh

%files
%defattr(-,root,root)
%doc README.md
%{_sysconfdir}/hibinit-config.cfg
%{_unitdir}/hibinit-agent.service
%{_bindir}/hibinit-agent
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/sleepconf
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/sleep.sh
%{python2_sitelib}/*
%dir %{_localstatedir}/lib/hibinit-agent
%ghost %attr(0600,root,root) %{_localstatedir}/lib/hibinit-agent/hibernation-enabled

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post hibinit-agent.service

%preun
%systemd_preun hibinit-agent.service

%postun
%systemd_postun_with_restart hibinit-agent.service

%changelog
* Thu May 16 2024 Seth Carolan <secarola@amazon.com> - 1.0.9
- Confirm /dev/snapshot exists before updating resume parameters again. Parameters are already set via Grub config update.

* Wed Jan 31 2024 Jeff Kim <kjeffsh@amazon.com> - 1.0.8-1
- Refactoring agent for legibility & changing service type to simple

* Thu Dec 27 2023 Jeff Kim <kjeffsh@amazon.com> - 1.0.8
- Added better termination behaviour with a stop timeout of 2 minutes

* Wed Oct 18 2023 Jeff Kim <kjeffsh@amazon.com> - 1.0.7
- Changed message when removing swap file
- Adding btrfs-enabled to set No_COW and get offset using btrfs

* Thu Sep 28 2023 Deborshi Saha <ddebs@amazon.com> - 1.0.6
- Add initial Amazon Linux 2022 support
- Add pm-utils for required package
- Recreate the swap file if the current size is sufficiently larger
- Update /sys/power/resume_offset and /sys/power/resume only if present

* Mon May 24 2021 Mohamed Aboubakr <mabouba@amazon.com> - 1.0.5
- Adding spec file for suse Linux
- swapon with max priority when hibernating

* Mon May 24 2021 Mohamed Aboubakr <mabouba@amazon.com> - 1.0.4
- grub2 mkconfig before grub configuration update
- Update /sys/power after grub configuration update
- Adding dracut to recreate initramfs after config update

* Thu Jan 14 2021 Mohamed Aboubakr <mabouba@amazon.com> - 1.0.3
- Add python3 support
- Support Redhat 8 by adding spec file for redhat and more configuration for acpid
- Remove config no replace for files that do not exist in etc directory

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

