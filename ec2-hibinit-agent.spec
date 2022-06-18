Name:           ec2-hibinit-agent
Version:        1.0.2
Release:        3%{?dist}
Summary:        Hibernation setup utility for AWS EC2

Group:          System Environment/Daemons
License:         Apache 2.0
Source0:        ec2-hibinit-agent-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2 python2-devel systemd acpid
%{?systemd_requires}

Requires: acpid grubby
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

mkdir -p mkdir -p "%{buildroot}%{_unitdir}/acpid.service.d"
install -m0644 "%{_builddir}/%{name}-%{version}/acpid-override.conf" "%{buildroot}%{_unitdir}/acpid.service.d"

%files
%defattr(-,root,root)
%doc README.md
%{_sysconfdir}/hibinit-config.cfg
%{_unitdir}/hibinit-agent.service
%{_unitdir}/acpid.service.d/acpid-override.conf
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
