#
# Conditional build:
%bcond_without	apidocs		# API documentation (for devhelp)
#
Summary:	A library to rewrite HTTP URLs to HTTPS URLs
Summary(pl.UTF-8):	Biblioteka przepisująca URL-e HTTP na HTTPS
Name:		libhttpseverywhere
Version:	0.4.8
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libhttpseverywhere/0.4/%{name}-%{version}.tar.xz
# Source0-md5:	3d9ee367a50b73643884abf8f5a35e15
URL:		https://github.com/GNOME/libhttpseverywhere
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gobject-introspection-devel
BuildRequires:	json-glib-devel
BuildRequires:	libarchive-devel
BuildRequires:	libgee-devel >= 0.8
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.39.1
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	vala
BuildRequires:	valadoc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library enables you to leverage the power of HTTPSEverywhere to
any desktop-application you want.

HTTPSEverywhere is a browser plugin that comes with a set of rules
that you can use to ensure that you use HTTP instead of HTTPS only
when this is absolutely not circumventable. With libhttpseverywhere
you will get a C-bindable, GLib-based library you can link/bind
against in almost all languages.

As a library written in Vala, libhttpseverywhere will support
GObject-Introspection. This means that you can use the lib in many
popular languages like e.g. Ruby, Python or JavaScript.

%description -l pl.UTF-8
Ta biblioteka pozwala na uzyskanie mocy HTTPSEverywhere w dowolnej
aplikacji desktopowej.

HTTPSEverywhere to wtyczka przeglądarki z zestawem reguł
zapewniających używanie HTTP zamiast HTTPS wyłącznie wtedy, gdy nie
daje się tego obejść. Dzięki libhttpseverywhere uzyskujemy opartą na
GLibie bibliotekę z dostępnym z poziomu C API, które można wykorzystać
w prawie dowolnym języku.

Jako biblioteka napisana w języku Vala, libhttpseverywhere obsługuje
GObject-Introspection. Oznacza to, że można jej używać w wielu
popularnych językach, np. Rubym, Pythonie czy JavaScripcie.

%package devel
Summary:	Header files for HTTPSEverywhere library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HTTPSEverywhere
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	json-glib-devel
Requires:	libarchive-devel
Requires:	libgee-devel >= 0.8
Requires:	libsoup-devel >= 2.4
Requires:	libxml2-devel >= 2.0

%description devel
Header files for HTTPSEverywhere library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HTTPSEverywhere.

%package -n vala-libhttpseverywhere
Summary:	Vala API for HTTPSEverywhere library
Summary(pl.UTF-8):	API języka Vala do biblioteki HTTPSEverywhere
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
Requires:	vala-libgee >= 0.8

%description -n vala-libhttpseverywhere
Vala API for HTTPSEverywhere library.

%description -n vala-libhttpseverywhere -l pl.UTF-8
API języka Vala do biblioteki HTTPSEverywhere.

%package apidocs
Summary:	API documentation for HTTPSEverywhere library
Summary(pl.UTF-8):	Dokumentacja API biblioteki HTTPSEverywhere
Group:		Documentation
Requires:	devhelp
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for HTTPSEverywhere library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki HTTPSEverywhere.

%prep
%setup -q

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
meson build \
	--buildtype=plain \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	%{?with_apidocs:-Denable_valadoc=true}

ninja -C build -v

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT \
ninja -C build -v install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libhttpseverywhere-0.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhttpseverywhere-0.4.so.0
%{_libdir}/girepository-1.0/HTTPSEverywhere-0.4.typelib
%{_datadir}/libhttpseverywhere

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhttpseverywhere-0.4.so
%{_includedir}/httpseverywhere-0.4
%{_pkgconfigdir}/httpseverywhere-0.4.pc

%files -n vala-libhttpseverywhere
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/httpseverywhere-0.4.deps
%{_datadir}/vala/vapi/httpseverywhere-0.4.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_datadir}/devhelp/books/httpseverywhere-0.4
%endif