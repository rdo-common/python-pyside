%global prerelease beta1
%global runtests 1

Name:           python-pyside
Version:        1.0.0
Release:        0.1.%{prerelease}%{?dist}
Summary:        Python bindings for Qt4

Group:          Development/Languages
License:        LGPLv2
URL:            http://www.pyside.org
Source0:        http://www.pyside.org/files/pyside-qt4.7+%{version}~%{prerelease}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:  generatorrunner-devel
BuildRequires:  phonon-devel
BuildRequires:  python2-devel
BuildRequires:  qt4-devel
BuildRequires:  qt4-webkit-devel
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
Requires:       qt4-webkit-devel
Requires:       shiboken-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n pyside-qt4.7+%{version}~%{prerelease}

# Fix up unit tests to use lrelease-qt4
sed -i -e "s/lrelease /lrelease-qt4 /" tests/QtCore/translation_test.py


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
* Fri Nov 26 2010 Kalev Lember <kalev@smartlink.ee> - 1.0.0-0.1.beta1
- Update to 1.0.0~beta1

* Thu Oct 14 2010 Kalev Lember <kalev@smartlink.ee> - 0.4.2-1
- Update to 0.4.2
- Dropped upstreamed patches

* Sat Oct 02 2010 Kalev Lember <kalev@smartlink.ee> - 0.4.1-4
- Re-enabled phonon bindings

* Wed Sep 29 2010 jkeating - 0.4.1-3
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Kalev Lember <kalev@smartlink.ee> - 0.4.1-2
- Depend on qt4-webkit-devel instead of qt-webkit-devel

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
