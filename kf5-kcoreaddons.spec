#
# Conditional build:
%bcond_with	tests		# build with tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.116
%define		qtver		5.15.2
%define		kfname		kcoreaddons
Summary:	Utilities for core application functionality and accessing the OS
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	06e53a939ecfa3725eaaaa531a2a974f
Patch0:		flaky-tests.patch
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info >= 1.3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5Core >= %{qtver}
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
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}
#%patch0 -p1

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ie,tok}

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
##%dir %{_libdir}/qt5/plugins/namespace
##%attr(755,root,root) %{_libdir}/qt5/plugins/namespace/jsonplugin_cmake_macro.so
##%attr(755,root,root) %{_libdir}/qt5/plugins/namespace/pluginwithoutmetadata.so
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
%{_libdir}/cmake/KF5CoreAddons
%{_libdir}/libKF5CoreAddons.so
%{_libdir}/qt5/mkspecs/modules/qt_KCoreAddons.pri
