#
# Conditional build:
%bcond_without	apidocs		# API documentation (for devhelp)
#
Summary:	A library to rewrite HTTP URLs to HTTPS URLs
Summary(pl.UTF-8):	Biblioteka przepisująca URL-e HTTP na HTTPS
Name:		libhttpseverywhere
Version:	0.8.3
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libhttpseverywhere/0.8/%{name}-%{version}.tar.xz
# Source0-md5:	c2a029fe6adac0d27e393cd2cfe74c7f
Patch0:		%{name}-vala0.42.patch
URL:		https://gitlab.gnome.org/GNOME/libhttpseverywhere
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gobject-introspection-devel
BuildRequires:	json-glib-devel
BuildRequires:	libarchive-devel
BuildRequires:	libgee-devel >= 0.8
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.39.1
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	vala-libgee >= 0.8
%{?with_apidocs:BuildRequires:	valadoc}
BuildRequires:	xz
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
%patch0 -p1

%build
%meson build \
	%{?with_apidocs:-Denable_valadoc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libhttpseverywhere-0.8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhttpseverywhere-0.8.so.0
%{_libdir}/girepository-1.0/HTTPSEverywhere-0.8.typelib
%{_datadir}/libhttpseverywhere

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhttpseverywhere-0.8.so
%{_includedir}/httpseverywhere-0.8
%{_pkgconfigdir}/httpseverywhere-0.8.pc

%files -n vala-libhttpseverywhere
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/httpseverywhere-0.8.deps
%{_datadir}/vala/vapi/httpseverywhere-0.8.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_datadir}/devhelp/books/httpseverywhere-0.8
%endif
