Name:           ec2-hibinit-agent
Version:        1.0.0
Release:        1%{?dist}
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post hibinit-agent.service

%preun
%systemd_preun hibinit-agent.service

%postun
%systemd_postun hibinit-agent.service

%changelog
* Wed Oct 31 2018 Anchal Agarwal <anchalag@amazon.com> - 1.0.0-1
- Initial build
