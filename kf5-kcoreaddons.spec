#
# Conditional build:
%bcond_with	tests		# build with tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.80
%define		qtver		5.9.0
%define		kfname		kcoreaddons
Summary:	Utilities for core application functionality and accessing the OS
Name:		kf5-%{kfname}
Version:	5.80.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	a53809e009c2346fe1c2d3451d39f1cf
Patch0:		flaky-tests.patch
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	fam-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KCoreAddons provides classes built on top of QtCore to perform various
tasks such as manipulating mime types, autosaving files, creating
backup files, generating random sequences, performing text
manipulations such as macro replacement, accessing user information
and many more.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core >= %{qtver}
Requires:	cmake >= 2.6.0

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}
#%patch0 -p1

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%{?with_tests:%ninja_build test}

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/mime/packages/kde5.xml
%attr(755,root,root) %{_libdir}/libKF5CoreAddons.so.*.*.*
%ghost %{_libdir}/libKF5CoreAddons.so.5
%{_datadir}/qlogging-categories5/kcoreaddons.categories
%dir %{_datadir}/kf5/licenses
%{_datadir}/kf5/licenses/ARTISTIC
%{_datadir}/kf5/licenses/BSD
%{_datadir}/kf5/licenses/GPL_V2
%{_datadir}/kf5/licenses/GPL_V3
%{_datadir}/kf5/licenses/LGPL_V2
%{_datadir}/kf5/licenses/LGPL_V21
%{_datadir}/kf5/licenses/LGPL_V3
%{_datadir}/kf5/licenses/QPL_V1.0
%{_datadir}/qlogging-categories5/kcoreaddons.renamecategories

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/desktoptojson
%{_includedir}/KF5/KCoreAddons
%{_includedir}/KF5/kcoreaddons_version.h
%{_libdir}/cmake/KF5CoreAddons
%{_libdir}/libKF5CoreAddons.so
%{_libdir}/qt5/mkspecs/modules/qt_KCoreAddons.pri
