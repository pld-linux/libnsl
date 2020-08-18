#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Library containing NIS functions using TI-RPC (IPv6 enabled)
Summary(pl.UTF-8):	Biblioteka zawierająca funkcje NIS wykorzystujące TI-RPC (z obsługą IPv6)
Name:		libnsl
Version:	1.3.0
Release:	1
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/thkukuk/libnsl/releases
Source0:	https://github.com/thkukuk/libnsl/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	9214f674bd0c2bcfdd6c1da0cadb061f
URL:		https://github.com/thkukuk/libnsl
BuildRequires:	gettext-tools >= 0.19.2
BuildRequires:	libtirpc-devel >= 1.0.1
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	libtirpc >= 1.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the libnsl library. This library contains the
public client interface for NIS(YP) and NIS+.

This code was formerly part of glibc, but is now standalone to be able
to link against TI-RPC for IPv6 support.

The NIS(YP) functions are still maintained, the NIS+ part is
deprecated and should not be used anymore.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę libnsl. Zawiera ona publiczny interfejs
klienta dla protokołów NIS(YP) oraz NIS+.

Kod wcześniej był częścią glibc, ale obecnie jest samodzielny, aby móc
korzystać z TI-RPC na potrzeby obsługi IPv6.

Funkcje NIS(YP) są nadal utrzymywane, natomiast część NIS+ jest
przestarzała i nie powinna być już używana.

%package devel
Summary:	Header files for libnsl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnsl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# libnsl used to be part of glibc
Requires:	glibc-devel >= 6:2.32
Requires:	libtirpc-devel >= 1.0.1

%description devel
Header files for libnsl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnsl.

%package static
Summary:	Static libnsl library
Summary(pl.UTF-8):	Statyczna biblioteka libnsl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnsl library.

%description static -l pl.UTF-8
Statyczna biblioteka libnsl.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libnsl.so.* $RPM_BUILD_ROOT/%{_lib}
ln -snf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libnsl.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libnsl.so

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnsl.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) /%{_lib}/libnsl.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libnsl.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnsl.so
%{_includedir}/rpcsvc/nis.h
%{_includedir}/rpcsvc/nis_callback.h
%{_includedir}/rpcsvc/nis_tags.h
%{_includedir}/rpcsvc/nislib.h
%{_includedir}/rpcsvc/yp.h
%{_includedir}/rpcsvc/yp_prot.h
%{_includedir}/rpcsvc/ypclnt.h
%{_includedir}/rpcsvc/yppasswd.h
%{_includedir}/rpcsvc/ypupd.h
%{_includedir}/rpcsvc/nis.x
%{_includedir}/rpcsvc/nis_callback.x
%{_includedir}/rpcsvc/nis_object.x
%{_includedir}/rpcsvc/yp.x
%{_includedir}/rpcsvc/yppasswd.x
%{_pkgconfigdir}/libnsl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnsl.a
%endif
