%define		tarball_name %{name}-ppl
Summary:	The Chunky Loop Generator
Name:		cloog
Version:	0.15.11
Release:	1
License:	GPL v2+
Group:		Libraries
URL:		http://www.cloog.org/
Source0:	ftp://gcc.gnu.org/pub/gcc/infrastructure/%{tarball_name}-%{version}.tar.gz
# Source0-md5:	060ae4df6fb8176e021b4d033a6c0b9e
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel >= 4.1.3
BuildRequires:	gmp-c++-devel >= 4.1.3
BuildRequires:	libtool
BuildRequires:	libtool
BuildRequires:	ppl-devel >= 0.10
BuildRequires:	texinfo >= 4.12
Requires(post):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CLooG is a software which generates loops for scanning Z-polyhedra.
That is, CLooG finds the code or pseudo-code where each integral point
of one or more parametrized polyhedron or parametrized polyhedra union
is reached. CLooG is designed to avoid control overhead and to produce
a very efficient code.

%package ppl
Summary:	Parma Polyhedra Library backend (ppl) based version of the Cloog binaries
Group:		Development/Libraries

%description ppl
The dynamic shared libraries of the Chunky Loop Generator

%package ppl-devel
Summary:	Development tools for the ppl based version of Chunky Loop Generator
Group:		Development/Libraries
Requires:	%{name}-ppl = %{version}-%{release}
Requires:	gmp-devel >= 4.1.3
Requires:	ppl-devel >= 0.10

%description ppl-devel
The header files and dynamic shared libraries of the Chunky Loop
Generator.

%prep
%setup -q -n %{tarball_name}-%{version}

sed -i -e s/ppl_minor_version=10/ppl_minor_version=11/  configure*

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--with-ppl

# Remove the cloog.info in the tarball
# to force the re-generation of a new one
test -f doc/cloog.info && rm doc/cloog.info

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post ppl	-p /sbin/postshell
/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%preun ppl
if [ "$1" = 0 ]; then
	[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
fi

%postun ppl -p /sbin/ldconfig

%files ppl
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root) %{_bindir}/cloog
%{_libdir}/libcloog.so.*
%{_infodir}/cloog.info*

%files ppl-devel
%defattr(644,root,root,755)
%{_includedir}/cloog
%{_libdir}/libcloog.so
