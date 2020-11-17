%{?python_enable_dependency_generator}

%global modulenames     ec2hibernatepolicy
%global selinuxtype     targeted
%global moduletype      services
%global gittag          %{version}
%global project         amazon-ec2-hibinit-agent

%global active_tuned_profile  $(cat %{_sysconfdir}/tuned/active_profile)
 
# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

Name:           ec2-hibinit-agent
Version:        1.0.3
Release:        3%{?dist}
Summary:        Hibernation setup utility for Amazon EC2

License:        ASL 2.0

Source0:        https://github.com/aws/%{project}/archive/v%{gittag}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: systemd-rpm-macros
BuildRequires: python3-devel
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel

%{?selinux_requires}
Requires: acpid 
Requires: grubby 
Requires: systemd 
Requires: tuned

%description
An EC2 agent that creates a setup for instance hibernation

%prep
%autosetup -n %{project}-%{gittag}
 
%build
%py3_build

# Makefile generates pp.bz2 from .tt file. 
# Generating tt file https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/security-enhanced_linux-the-sepolicy-suite-sepolicy_generate
make -C %{_builddir}/%{project}-%{gittag}/packaging/rhel/ec2hibernatepolicy

%install
%py3_install

mkdir -p %{buildroot}%{python3_sitelib}
mkdir -p "%{buildroot}%{_unitdir}"
mkdir -p %{buildroot}%{_sysconfdir}/acpi/events 
mkdir -p %{buildroot}%{_localstatedir}/lib/hibinit-agent
mkdir -p %{buildroot}%{_sysconfdir}/acpi/actions

install -p -m 644 "%{_builddir}/%{project}-%{gittag}/hibinit-agent.service" %{buildroot}%{_unitdir}
install -p -m 644 "%{_builddir}/%{project}-%{gittag}/acpid.sleep.conf" %{buildroot}%{_sysconfdir}/acpi/events/sleepconf

mkdir -p %{buildroot}%{_prefix}/lib/systemd/logind.conf.d
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-sleep

install -p -m 644 "%{_builddir}/%{project}-%{gittag}/etc/hibinit-config.cfg" %{buildroot}/%{_sysconfdir}/hibinit-config.cfg
install -p -m 644 "%{_builddir}/%{project}-%{gittag}/packaging/rhel/00-hibinit-agent.conf" %{buildroot}%{_prefix}/lib/systemd/logind.conf.d/00-hibinit-agent.conf
install -p -m 755 "%{_builddir}/%{project}-%{gittag}/packaging/rhel/acpid.sleep.sh" %{buildroot}%{_sysconfdir}/acpi/actions/sleep.sh
install -p -m 755 "%{_builddir}/%{project}-%{gittag}/packaging/rhel/sleep-handler.sh" %{buildroot}%{_prefix}/lib/systemd/system-sleep/sleep-handler.sh

#Disable transparent huge page
mkdir -p  %{buildroot}%{_sysconfdir}/tuned/nothp_profile
install -p -m 644 "%{_builddir}/%{project}-%{gittag}/packaging/rhel/tuned.conf" %{buildroot}%{_sysconfdir}/tuned/nothp_profile/tuned.conf

# Install policy modules
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 %{_builddir}/%{project}-%{gittag}/packaging/rhel/ec2hibernatepolicy/$MODULES \
        %{buildroot}%{_datadir}/selinux/packages


%files
%doc README.md
%license LICENSE.txt

%{_sysconfdir}/hibinit-config.cfg
%{_unitdir}/hibinit-agent.service
%{_bindir}/hibinit-agent
%config(noreplace) %{_sysconfdir}/acpi/events/sleepconf
%config(noreplace) %{_sysconfdir}/acpi/actions/sleep.sh
%{python3_sitelib}/ec2_hibinit_agent-*.egg-info/
%dir %{_localstatedir}/lib/hibinit-agent
%ghost %attr(0600,root,root) %{_localstatedir}/lib/hibinit-agent/hibernation-enabled

%dir %{_prefix}/lib/systemd/logind.conf.d
%dir %{_prefix}/lib/systemd/system-sleep

%dir %{_sysconfdir}/tuned/nothp_profile
%config(noreplace) %{_sysconfdir}/tuned/nothp_profile/tuned.conf

%config(noreplace) %{_prefix}/lib/systemd/system-sleep/sleep-handler.sh
%config(noreplace) %{_prefix}/lib/systemd/logind.conf.d/00-hibinit-agent.conf
%attr(0644,root,root) %{_datadir}/selinux/packages/*.pp.bz2

%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%systemd_post hibinit-agent.service

#
# Install all modules in a single transaction
#
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
%selinux_modules_install -s %{selinuxtype} $MODULES

#
# Disable THP by switching to  nothp_profile profile
#
sed -i'' "s/^[#]*\s*include=.*/include=%{active_tuned_profile}/" %{_sysconfdir}/tuned/nothp_profile/tuned.conf
tuned-adm profile nothp_profile


%preun
%systemd_preun hibinit-agent.service

#
# Enable THP by switching to nothp_profile profile
#
tuned-adm profile $(sed -n 's/^include=//p' %{_sysconfdir}/tuned/nothp_profile/tuned.conf)
# note that tuned is not enabled and needs to be enabled. 

%postun
%systemd_postun_with_restart hibinit-agent.service

# https://fedoraproject.org/wiki/SELinux/IndependentPolicy
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} $MODULES
fi


%posttrans
%selinux_relabel_post -s %{selinuxtype}

%changelog
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
