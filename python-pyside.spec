%global runtests 1

Name:           python-pyside
Version:        0.4.1
Release:        1%{?dist}
Summary:        Python bindings for Qt4

Group:          Development/Languages
License:        LGPLv2
URL:            http://www.pyside.org
Source0:        http://www.pyside.org/files/pyside-qt4.6+%{version}.tar.bz2
# Don't override cmake release type to avoid -O3 optimization level
Patch0:         python-pyside-release-type.patch
# Don't use xvfb-run which is currently broken in Fedora
# https://bugzilla.redhat.com/show_bug.cgi?id=632879
Patch1:         python-pyside-disable_xvfb-run.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  generatorrunner-devel
# http://bugs.openbossa.org/show_bug.cgi?id=355
#BuildRequires:  phonon-devel
BuildRequires:  python2-devel
BuildRequires:  qt4-devel
BuildRequires:  qt-webkit-devel
BuildRequires:  shiboken-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-xauth

# Don't want provides for python shared objects
%{?filter_provides_in: %filter_provides_in %{python_sitearch}/PySide/.*\.so}
%{?filter_setup}

%description
PySide provides Python bindings for the Qt cross-platform application
and UI framework. PySide consists of a full set of Qt bindings, being
compatible with PyQt4 API 2.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       cmake
Requires:       phonon-devel
Requires:       python2-devel
Requires:       qt4-devel
Requires:       qt-webkit-devel
Requires:       shiboken-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n pyside-qt4.6+%{version}

# Fix up unit tests to use lrelease-qt4
sed -i -e "s/lrelease /lrelease-qt4 /" tests/QtCore/translation_test.py

%patch0 -p1 -b .release_type
%patch1 -p1 -b .disable_xvfb-run


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} -DCMAKE_SKIP_RPATH=true ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

# Fix permissions
chmod 755 $RPM_BUILD_ROOT%{python_sitearch}/PySide/*.so

%check
%if 0%{?runtests}
# Tests need an X server
export DISPLAY=:21
Xvfb $DISPLAY &
trap "kill $! ||:" EXIT
sleep 3

pushd %{_target_platform}
ctest -V ||:
popd
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING PySide/licensecomment.txt
%{_libdir}/libpyside.so.*
%{python_sitearch}/PySide/

%files devel
%defattr(-,root,root,-)
%{_includedir}/PySide/
%{_libdir}/libpyside.so
%{_libdir}/cmake/PySide-%{version}/
%{_libdir}/pkgconfig/pyside.pc
%{_datadir}/PySide/


%changelog
* Sat Sep 11 2010 Kalev Lember <kalev@smartlink.ee> - 0.4.1-1
- Update to 0.4.1
- Added patch to disable xvfb-run which is currently broken (#632879)
- Disabled phonon bindings (PySide bug #355)
- License change from LGPLv2 with exceptions to LGPLv2

* Sun Aug 15 2010 Kalev Lember <kalev@smartlink.ee> - 0.4.0-3
- Review related fixes (#623425)
- Include PySide/licensecomment.txt

* Thu Aug 12 2010 Kalev Lember <kalev@smartlink.ee> - 0.4.0-2
- Added missing phonon-devel and qt-webkit-devel deps (#623425)

* Wed Aug 11 2010 Kalev Lember <kalev@smartlink.ee> - 0.4.0-1
- Initial RPM release
