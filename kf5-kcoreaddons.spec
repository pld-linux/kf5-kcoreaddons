#
# Conditional build:
%bcond_without	tests		# build without tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.10
%define		qtver		5.3.2
%define		kfname		kcoreaddons
Summary:	Utilities for core application functionality and accessing the OS
Name:		kf5-%{kfname}
Version:	5.10.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	17142e16ed6e396771f5ae7e890d1084
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	fam-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
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

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
        DESTDIR=$RPM_BUILD_ROOT

%find_lang %{kfname}5_qt --with-qm --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/mime/packages/kde5.xml
%attr(755,root,root) %{_libdir}/libKF5CoreAddons.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5CoreAddons.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/desktoptojson
%{_includedir}/KF5/KCoreAddons
%{_includedir}/KF5/kcoreaddons_version.h
%{_libdir}/cmake/KF5CoreAddons
%attr(755,root,root) %{_libdir}/libKF5CoreAddons.so
%{_libdir}/qt5/mkspecs/modules/qt_KCoreAddons.pri
