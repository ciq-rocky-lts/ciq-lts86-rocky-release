# CIQ Rocky Linux LTS 8.6 release package

# This package should be almost identical to the final released Rocky 8.6 -release package, but 
# includes .repo files that point to dl.rockylinux.org/vault/ instead of the default mirrorlist entries

# CIQ may customize this package in the future to enhance the LTS 8.6 experience

%define debug_package %{nil}

# Product information
%define product_family Rocky Linux
%define variant_titlecase Server
%define variant_lowercase server

# Distribution Name and Version
%define distro_name  Rocky Linux
%define distro_code  Green Obsidian
%define major   8
%define minor   6
%define rocky_rel 6
%define upstream_rel %{major}.%{minor}
%define rpm_license  BSD-3-Clause

%define base_release_version %{major}
%define full_release_version %{major}
%define dist_release_version %{major}

%ifarch ppc64le
%define tuned_profile :server
%endif

# Avoids a weird anaconda problem
%global __requires_exclude_from %{_libexecdir}

Name:           ciq-lts86-rocky-release
Version:        %{major}.%{minor}
Release:        %{rocky_rel}.el8
Summary:        %{distro_name} release files
License:        %{rpm_license}
URL:            https://rockylinux.org
BuildArch:      noarch

# What do we provide?
Provides:       rocky-release = %{version}-%{release}
Provides:       rocky-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{version}-%{release}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{major}
Provides:       centos-release = %{version}-%{release}
Provides:       centos-release(upstream) = %{upstream_rel}

## Required by libdnf
Provides:       base-module(platform:el%{major})

## This makes lorax/pungi/anaconda happy
Provides:       rocky-release-eula
Provides:       redhat-release-eula
Provides:       centos-release-eula



# Stocky rocky-repos and ciq-rocky86-repos should be provided by the CIQ specific repos package
Requires: ciq-rocky86-repos(%{major})
Requires: rocky-repos(%{major})

# CIQ LTS 8.6 packages should obsolete and conflict with the canonical rocky-release package:
Obsoletes: rocky-release
Conflicts: rocky-release


# GPG Keys
Source101:      RPM-GPG-KEY-rockyofficial
Source102:      RPM-GPG-KEY-rockytesting

# Release Sources
Source200:      EULA
Source201:      LICENSE
Source202:      Contributors
Source203:      COMMUNITY-CHARTER
Source300:      85-display-manager.preset
Source301:      90-default.preset
Source302:      99-default-disable.preset

# Repo Sources
Source1200:     Rocky-BaseOS.repo
Source1201:     Rocky-AppStream.repo
Source1202:     Rocky-PowerTools.repo
Source1203:     Rocky-Extras.repo

# Rocky Add-ons
Source1210:     Rocky-HighAvailability.repo
Source1211:     Rocky-ResilientStorage.repo
Source1212:     Rocky-RT.repo
Source1213:     Rocky-NFV.repo

# Rocky Special Stuff
Source1220:     Rocky-Media.repo
Source1221:     Rocky-Debuginfo.repo
Source1222:     Rocky-Sources.repo
Source1223:     Rocky-Devel.repo
Source1226:     Rocky-Plus.repo
Source1300:     rocky.1.gz

%description
%{distro_name} release files.

%package -n ciq-rocky86-repos
Summary:        %{distro_name} Package Repositories
License:        %{rpm_license}
Provides:       rocky-repos(%{major}) = %{upstream_rel}
Requires:       system-release = %{upstream_rel}
Requires:       rocky-gpg-keys
Conflicts:      %{name} < 8.0


# CIQ 8.6 specific: We conflict with the original rocky-repos, we want to force the 8.6 vault to be used
Provides: ciq-rocky86-repos(%{major}) = %{upstream_rel}
Conflicts: rocky-repos     
Obsoletes: rocky-repos

# We also obsolete ciq-rocky-repos if a user has that installed.  There can be only 1 -repos package:
Conflicts: ciq-rocky-repos
Obsoletes: ciq-rocky-repos

%description -n ciq-rocky86-repos
%{distro_name} package repository files for yum/dnf

%package -n rocky-gpg-keys
Summary:        Rocky RPM GPG Keys
Conflicts:      %{name} < 8.0

%description -n rocky-gpg-keys
This package provides the RPM signature keys for Rocky.

%prep
echo Good.

%build
echo Good.

%install
# copy license and contributors doc here for %%license and %%doc macros
cp %{SOURCE201} %{SOURCE202} %{SOURCE203} .

# create /etc/system-release and /etc/redhat-release
install -d -m 0755 %{buildroot}%{_sysconfdir}
echo "%{distro_name} release %{version} (%{distro_code})" > %{buildroot}%{_sysconfdir}/rocky-release
echo "Derived from Red Hat Enterprise Linux %{version}" > %{buildroot}%{_sysconfdir}/rocky-release-upstream
ln -s rocky-release %{buildroot}%{_sysconfdir}/system-release
ln -s rocky-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s rocky-release %{buildroot}%{_sysconfdir}/centos-release
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE1300} %{buildroot}%{_mandir}/man1/

# Create the os-release file
install -d -m 0755 %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="%{distro_name}"
VERSION="%{major}.%{minor} (%{distro_code})"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="%{major}.%{minor}"
PLATFORM_ID="platform:el%{major}"
PRETTY_NAME="%{distro_name} %{major}.%{minor} (%{distro_code})"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:rocky:rocky:%{base_release_version}:GA"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
ROCKY_SUPPORT_PRODUCT="%{distro_name}"
ROCKY_SUPPORT_PRODUCT_VERSION="%{major}"
REDHAT_SUPPORT_PRODUCT="%{distro_name}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{major}"
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:rocky:rocky:%{base_release_version}:GA" > %{buildroot}%{_sysconfdir}/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}%{_sysconfdir}/issue
echo 'Kernel \r on an \m' >> %{buildroot}%{_sysconfdir}/issue
cp %{buildroot}%{_sysconfdir}/issue{,.net}
echo >> %{buildroot}%{_sysconfdir}/issue

# set up the dist tag macros
install -d -m 0755 %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.dist << EOF
# dist macros.

%%__bootstrap ~bootstrap
%%rocky_ver %{major}
%%rocky %{major}
%%centos_ver %{major}
%%centos %{major}
%%rhel %{major}
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.el%{major}%%{?with_bootstrap:%{__bootstrap}}
%%el%{major} 1
EOF

# Data directory
install -d -m 0755 %{buildroot}%{_datadir}/rocky-release
ln -s rocky-release %{buildroot}%{_datadir}/redhat-release
install -p -m 0644 %{SOURCE200} %{buildroot}%{_datadir}/rocky-release/

# systemd presets
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE300} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE301} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE302} %{buildroot}/%{_prefix}/lib/systemd/system-preset/

# dnf stuff
install -d -m 0755 %{buildroot}%{_sysconfdir}/dnf/vars
echo "pub/rocky" > %{buildroot}%{_sysconfdir}/dnf/vars/contentdir
echo "pub/sig" > %{buildroot}%{_sysconfdir}/dnf/vars/sigcontentdir
echo "%{major}-stream" > %{buildroot}%{_sysconfdir}/dnf/vars/stream

# Copy out GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p -m 0644 %{SOURCE101} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/
install -p -m 0644 %{SOURCE102} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

# Copy our yum repos
install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -p -m 0644 %{SOURCE1200} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1201} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1202} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1203} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1210} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1211} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1212} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1213} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1220} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1221} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1222} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1223} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE1226} %{buildroot}%{_sysconfdir}/yum.repos.d/

%files
%license LICENSE
%doc Contributors COMMUNITY-CHARTER
%{_sysconfdir}/redhat-release
%{_sysconfdir}/centos-release
%{_sysconfdir}/system-release
%{_sysconfdir}/rocky-release
%{_sysconfdir}/rocky-release-upstream
%config(noreplace) %{_sysconfdir}/os-release
%config %{_sysconfdir}/system-release-cpe
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%{_sysconfdir}/rpm/macros.dist
%{_datadir}/redhat-release
%{_datadir}/rocky-release
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*
%{_mandir}/man1/rocky.1.gz

%files -n ciq-rocky86-repos
%license LICENSE
%config(noreplace) %{_sysconfdir}/yum.repos.d/Rocky-*.repo
%config(noreplace) %{_sysconfdir}/dnf/vars/contentdir
%config(noreplace) %{_sysconfdir}/dnf/vars/sigcontentdir
%config(noreplace) %{_sysconfdir}/dnf/vars/stream

%files -n rocky-gpg-keys
%{_sysconfdir}/pki/rpm-gpg/

%changelog
* Fri Feb 10 2023 Skip Grube <sgrube@ciq.co> - 8.6-6
- Fixed issues in source repository URLs

* Sat Dec 10 2022 Skip Grube <sgrube@ciq.co> - 8.6-5
- Building CIQ-specific 8.6 release for Long Term Support updates (LTS 8.6)

* Tue Aug 30 2022 Louis Abel <label@rockylinux.org> - 8.6-4
- Add stream dnf var

* Fri May 20 2022 Louis Abel <label@rockylinux.org> - 8.6-3
- Add pub/sig var for dnf

* Tue Mar 29 2022 Louis Abel <label@rockylinux.org> - 8.6-2
- 8.6 prepatory release
- Add REDHAT_SUPPORT_PRODUCT to /etc/os-release

* Mon Feb 14 2022 Louis Abel <label@rockylinux.org> - 8.5-4
- Add bootstrap to macros to match EL9

* Tue Dec 21 2021 Louis Abel <label@rockylinux.org> - 8.5-3
- Add countme=1 to base repositories

* Sat Dec 11 2021 Louis Abel <label@rockylinux.org> - 8.5-2
- Fix CPE to match upstreamed Rocky data

* Tue Oct 05 2021 Louis Abel <label@rockylinux.org> - 8.5-1
- 8.5 prepatory release

* Mon Sep 13 2021 Louis Abel <label@rockylinux.org> - 8.4-35
- Add missing CentOS provides and symlinks
- Add centos macros for some builds to complete successfully without relying
  on random patching

* Thu Sep 09 2021 Louis Abel <label@rockylinux.org> - 8.4-33
- Add centos as an id_like to allow current and future SIGs that rely on CentOS
  to work properly.

* Wed Jul 07 2021 Louis Abel <label@rockylinux.org> - 8.4-32
- Fix URLs for Plus and NFV
- Use a macro for the license across sub packages
- Fix bogus date in changelog

* Mon Jul 05 2021 Louis Abel <label@rockylinux.org> - 8.4-30
- Fix URLs for debuginfo

* Tue Jun 29 2021 Louis Abel <label@rockylinux.org> - 8.4-29
- Fix URLs
- Added debuginfo
- Added NFV (future state)

* Wed Jun 16 2021 Louis Abel <label@rockylinux.org> - 8.4-25
- Fix up outstanding issues

* Sat Jun 05 2021 Louis Abel <label@rockylinux.org> - 8.4-24
- Change all mirrorlist urls to https

* Tue May 25 2021 Louis Abel <label@rockylinux.org> - 8.4-23
- Add a version codename to satisfy vendors
- Change license
- Fix up /etc/os-release and CPE
- Remove unused infra var
- Change base_release_version to major

* Wed May 19 2021 Louis Abel <label@rockylinux.org> - 8.4-16
- Remove annoying /etc/issue banner

* Sat May 08 2021 Louis Abel <label@rockylinux.org> - 8.4-15
- Release for 8.4

* Wed May 05 2021 Louis Abel <label@rockylinux.org> - 8.3-14
- Add RT, Plus, and NFV repo files

* Mon May 03 2021 Louis Abel <label@rockylinux.org> - 8.3-13
- Add minor version to /etc/os-release to resolve issues
  with products that provide the "full version"

* Sat May 01 2021 Louis Abel <label@rockylinux.org> - 8.3-12
- Add resilient storage varient
- Fix vars

* Wed Apr 28 2021 Louis Abel <label@rockylinux.org> - 8.3-11
- Fix repo URL's where needed
- Change contentdir var

* Sun Apr 25 2021 Louis Abel <label@rockylinux.org> - 8.3-9
- Remove and add os-release references

* Sun Apr 18 2021 Louis Abel <label@rockylinux.org> - 8.3-8
- Emphasize that this is not a production ready release
- rpmlint

* Wed Apr 14 2021 Louis Abel <label@rockylinux.org> - 8.3-7
- Fix mantis links

* Thu Apr 08 2021 Louis Abel <label@rockylinux.org> - 8.3-5
- Combine release, repos, and keys together to simplify

* Mon Feb 01 2021 Louis Abel <label@rockylinux.org> - 8.3-4
- Initial Rocky Release 8.3 based on CentOS 8.3
- Keep centos rpm macro to reduce package modification burden
- Update /etc/issue
