%define migtools_version 45
%define db_version 4.2.52
%define db_version_40 4.0.14
%define ldbm_backend berkeley
%define version_20 2.0.27
%define version_21 2.1.30
%define version_22 2.2.13
%define evolution_connector_prefix %{_libdir}/evolution-openldap
%define evolution_connector_includedir %{evolution_connector_prefix}/include
%define evolution_connector_libdir %{evolution_connector_prefix}/%{_lib}
# For Fedora, we want 2.1 compatibility.  For RHEL or RHL9, we may want 2.0.
%define compat_version %{version_21}
%define nptl_arches %{ix86} ia64 ppc ppc64 s390 s390x sparcv9 x86_64

Summary: The configuration files, libraries, and documentation for OpenLDAP.
Name: openldap
Version: %{version_22}
Release: 6.4E
License: OpenLDAP
Group: System Environment/Daemons
Source0: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version_22}.tgz
Source1: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version_20}.tgz
Source2: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version_21}.tgz
Source3: ftp://ftp.OpenLDAP.org/pub/tools/autoconf-2.13.1.tar.gz
Source4: ftp://ftp.OpenLDAP.org/pub/tools/automake-1.4a.tar.gz
Source5: http://www.sleepycat.com/update/snapshot/db-%{db_version}.tar.gz
Source6: http://www.sleepycat.com/update/snapshot/db-%{db_version_40}.tar.gz
Source7: ldap.init
Source8: ftp://ftp.padl.com/pub/MigrationTools-%{migtools_version}.tar.gz
Source9: migration-tools.txt
Source10: autofs.schema
Source11: README.upgrading
Source12: http://www.OpenLDAP.org/doc/admin/guide.html
Source13: nptl-abi-note.S
Source14: README.evolution
Patch0: openldap-2.2.13-config.patch
Patch2: openldap-1.2.11-cldap.patch
Patch3: openldap-2.1.17-syslog.patch
Patch4: openldap-2.0.11-ldaprc.patch
Patch5: openldap-2.2.13-setugid.patch
Patch6: openldap-2.2.13-pie.patch
Patch7: openldap-2.2.13-toollinks.patch
Patch8: openldap-2.2.13-nosql.patch
Patch9: openldap-2.1.30-ldapi.patch
Patch10: openldap-2.2.13-3201.patch
Patch11: openldap-2.2.13-dryrun.patch
Patch12: db-4.0.14-disable-mutex.patch
Patch13: db-4.0.14-libobjs.patch
Patch21: MigrationTools-38-instdir.patch
Patch22: MigrationTools-36-mktemp.patch
Patch23: MigrationTools-27-simple.patch
Patch24: MigrationTools-26-suffix.patch
Patch25: MigrationTools-44-schema.patch
Patch30: http://www.sleepycat.com/update/4.2.52/patch.4.2.52.1
Patch31: http://www.sleepycat.com/update/4.2.52/patch.4.2.52.2
Patch40: openldap-ntlm.diff
Patch41: openldap-2.2.13-tls-fix-connection-test.patch
Patch42: openldap-2.2.13-hop.patch
Patch43: openldap-2.0.27-hop.patch
Patch44: openldap-2.1.30-hop.patch
Patch45: openldap-2.2.13-nostrip.patch
Patch46: openldap-2.2.13-wait4msg-select-fix.patch
Patch47: openldap-2.2.13-gethostbyname_r.patch

URL: http://www.openldap.org/
BuildRoot: %{_tmppath}/%{name}-%{version_22}-root
BuildPreReq: cyrus-sasl-devel >= 2.1, gdbm-devel, libtool >= 1.5.6-2, krb5-devel
BuildPreReq: openssl-devel, pam-devel, perl, pkgconfig, tcp_wrappers,
BuildPreReq: unixODBC-devel
Requires: cyrus-sasl, cyrus-sasl-md5, mktemp

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package devel
Summary: OpenLDAP development libraries and header files.
Group: Development/Libraries
Requires: openldap = %{version_22}-%{release}, cyrus-sasl-devel >= 2.1
Provides: openldap-evolution-devel = %{version_22}-%{release}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package servers
Summary: OpenLDAP servers and related files.
Prereq: fileutils, make, openldap = %{version_22}-%{release}, openssl, /usr/sbin/useradd, /sbin/chkconfig
Group: System Environment/Daemons

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd and slurpd servers,
migration scripts, and related files.

%package servers-sql
Summary: OpenLDAP server SQL support module.
Prereq: openldap-servers = %{version_22}-%{release}
Group: System Environment/Daemons

%description servers-sql
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains a loadable module which the
slapd server can use to read data from an RDBMS.

%package clients
Summary: Client programs for OpenLDAP.
Prereq: openldap = %{version_22}-%{release}
Group: Applications/Internet

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.

# Declare this subpackage LAST.  This version tag redefines %%{version}, so
# any future use would reference the wrong version.
%package -n compat-openldap
Summary: OpenLDAP compatibility shared libraries.
Group: System Environment/Libraries
Requires: openldap = %{version_22}-%{release}, cyrus-sasl >= 2.1
Version: %{compat_version}

%description -n compat-openldap
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools.  The compat-openldap package
includes older versions of the OpenLDAP shared libraries which may be
required by some applications.

%prep
%setup -q -c -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 8

pushd openldap-%{version_22}
%patch0 -p1 -b .config
%patch2 -p1 -b .cldap
%patch3 -p1 -b .syslog
%patch4 -p1 -b .ldaprc
%patch5 -p1 -b .setugid
%patch6 -p1 -b .pie
%patch7 -p1 -b .toollinks
%patch8 -p1 -b .nosql
%patch10 -p0 -b .3201
%patch11 -p0 -b .dryrun
%patch41 -p1 -b .CAN-2005-2069
%patch42 -p1 -b .hop
%patch46 -p1 -b .wait4msg-select-fix
%patch47 -p1 -b .gethostbyname_r

cp %{_datadir}/libtool/config.{sub,guess} build/
popd

# Set up a build tree for a static version of libldap with the hooks for the
# non-standard NTLM bind type which is needed to connect to Win2k GC servers
# (Win2k3 supports SASL with DIGEST-MD5, so this shouldn't be needed for those
# servers, though as of version 1.4 the connector doesn't try SASL first).
cp -a openldap-%{version_22} evo-openldap-%{version_22}
pushd evo-openldap-%{version_22}
%patch40 -p0 -b .evolution-ntlm
popd

pushd db-%{db_version_40}
%patch12 -p1 -b .disable-mutex
%patch13 -p1 -b .libobj
cd dist
./s_config
popd

pushd db-%{db_version}
%patch30 -b .db-1
%patch31 -b .db-2
popd

pushd MigrationTools-%{migtools_version}
%patch21 -p1 -b .instdir
%patch22 -p1 -b .mktemp
%patch23 -p1 -b .simple
%patch24 -p1 -b .suffix
%patch25 -p1 -b .schema
popd

pushd openldap-%{version_20}
%patch43 -p1 -b .hop

	for subdir in build-gdbm build-db build-clients build-compat ; do
		mkdir $subdir
		ln -s ../configure $subdir
	done
popd

pushd openldap-%{version_21}
%patch9 -p1 -b .ldapi
%patch44 -p1 -b .hop
	for subdir in build-servers build-compat ; do
		mkdir $subdir
		ln -s ../configure $subdir
	done
popd

pushd openldap-%{version_22}
	for subdir in build-servers build-clients ; do
		mkdir $subdir
		ln -s ../configure $subdir
	done
popd

autodir=`pwd`/auto-instroot
pushd autoconf-2.13.1
./configure --prefix=$autodir
make all install
popd
pushd automake-1.4a
./configure --prefix=$autodir
make all install
popd

%patch45 -p1 -b .nostrip

%build
autodir=`pwd`/auto-instroot
dbdir=`pwd`/db-instroot
dbdir40=`pwd`/db-instroot-4.0
libtool='%{_bindir}/libtool'
tagname=CC; export tagname

PATH=${autodir}/bin:${PATH}

%ifarch ia64
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -O0 -DLDAP_PVT_THREAD_STACK_SIZE=8*1024*1024"
%endif

# Set CFLAGS to incorporate RPM_OPT_FLAGS.
CFLAGS="$RPM_OPT_FLAGS -D_REENTRANT -fPIC"; export CFLAGS

# Build the 2.0 server tools for dumping out old on-disk databases.  This
# requires Berkeley DB 4.0.x (which we must build) and gdbm.
pushd db-%{db_version_40}/dist
./configure -C \
	--with-pic \
	--disable-shared \
	--with-uniquename=_openldap_slapd_rhl_40 \
	--prefix=${dbdir40} \
	--includedir=${dbdir40}/include \
	--libdir=${dbdir40}/%{_lib}
make %{_smp_mflags}
make install
popd

# Set CPPFLAGS/CFLAGS/LDFLAGS to find our just-built DB 4.0.
CPPFLAGS="-I${dbdir40}/include" ; export CPPFLAGS
CFLAGS="$CPPFLAGS $RPM_OPT_FLAGS -D_REENTRANT -fPIC"; export CFLAGS
LDFLAGS="-L${dbdir40}/%{_lib}" ; export LDFLAGS

pushd openldap-%{version_20}/build-gdbm
%configure \
	--disable-shared \
	--without-cyrus-sasl \
	--without-kerberos \
	--without-threads \
	--without-tls \
	--enable-ldbm \
	--with-ldbm-api=gdbm \
	--program-suffix=-slapd-2.0-gdbm
make %{_smp_mflags}
popd

pushd openldap-%{version_20}/build-db
LIBS=-lpthread; export LIBS
%configure \
	--disable-shared \
	--without-cyrus-sasl \
	--without-kerberos \
	--without-threads \
	--without-tls \
	--enable-ldbm \
	--with-ldbm-api=berkeley \
	--program-suffix=-slapd-2.0-dbb
make %{_smp_mflags}
unset LIBS
popd

# Build Berkeley DB and install it into a temporary area, isolating OpenLDAP
# from any future changes to the system-wide Berkeley DB library.  Version 4.2
# or later is required by the BDB backend in OpenLDAP 2.1 and later.
buildbdb() {
	subdir=$1
	shift
	install -d db-%{db_version}/build-rpm${subdir:+-${subdir}}
	pushd db-%{db_version}/build-rpm${subdir:+-${subdir}}
	echo "${1:+db_cv_mutex=$1}" > config.cache
	shift
	../dist/configure -C \
		--with-pic \
		--disable-static \
		--enable-shared \
		--with-uniquename=_openldap_slapd_rhl_42 \
		--prefix=${dbdir} \
		--includedir=${dbdir}/include \
		--libdir=${dbdir}/%{_lib}${subdir:+/${subdir}}
	# XXX db-4.2.x handles O_DIRECT (by disabling on linux) correctly.
	# XXX hack out O_DIRECT support in db4 for now.
	perl -pi -e 's/#define HAVE_O_DIRECT 1/#undef HAVE_O_DIRECT/' db_config.h
	# fix libtool: no rpath
        perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool

	if test -n "$nptl_lo" ; then
		./libtool --mode=compile %{__cc} -o $nptl_lo -c $nptl_s
	fi
	make %{_smp_mflags} libdb_base=libslapd_db libso_base=libslapd_db LIBSO_LIBS="$nptl_lo"
	make install libdb_base=libslapd_db libso_base=libslapd_db LIBSO_LIBS="$nptl_lo"
	ln -sf libslapd_db.so ${dbdir}/%{_lib}/${subdir}/libdb.so
	popd
}

# Build an NPTL libdb if we're on a Linux arch with NPTL.  NPTL gives us the
# ability to share mutexes between threads in different processes, and to have
# threads in both honor those locks.  We have to do this because if you build
# libdb with support for intra-process locks, it dies if you don't have it and
# the application has specified to libdb that it's multi-threaded (as slapd
# does).
%ifarch %{nptl_arches}
unset nptl_s nptl_lo
case %{_os} in
linux|Linux)
	nptl_s=$RPM_SOURCE_DIR/nptl-abi-note.S
	nptl_lo=nptl-abi-note.lo
	;;
esac
buildbdb tls POSIX/pthreads/library
unset nptl_s nptl_lo
%endif

# Build a non-NPTL libdb and tools, able to only use intra-process thread
# locks.  Useless for bdb's purposes (bdb requires shared env support), but
# acceptable for ldbm.
buildbdb "" POSIX/pthreads/library/private

# Find OpenSSL's header and library dependencies.
if pkg-config openssl ; then
	OPENSSL_CPPFLAGS=`pkg-config --cflags-only-I openssl`
	CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
	OPENSSL_LDFLAGS=`pkg-config --libs-only-L openssl`
	LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS
fi
CPPFLAGS="-I${dbdir}/include $OPENSSL_CPPFLAGS" ; export CPPFLAGS
CFLAGS="$CPPFLAGS $RPM_OPT_FLAGS -D_REENTRANT -fPIC"; export CFLAGS
LDFLAGS="-L${dbdir}/%{_lib} $OPENSSL_LDFLAGS" ; export LDFLAGS

# Build the 2.1 server tools for dumping out old on-disk databases.  This
# requires Berkeley DB 4.3.x.
pushd openldap-%{version_21}/build-servers
LIBS=-lpthread; export LIBS
%configure \
	--disable-shared \
	--disable-dynamic \
	--without-cyrus-sasl \
	--without-kerberos \
	--without-threads \
	--without-tls \
	--enable-slapd --disable-slurpd \
	--enable-bdb \
	--enable-ldbm \
	--with-ldbm-api=%{ldbm_backend} \
	--program-suffix=-slapd-2.1
make %{_smp_mflags}
unset LIBS
popd

# Build the client libraries for the compat package.
pushd openldap-%{compat_version}/build-compat
%configure \
	--disable-slapd --disable-slurpd \
	--with-threads=posix --disable-static --enable-shared --enable-dynamic \
	--enable-local --enable-rlookups --with-tls --with-cyrus-sasl \
	--without-kerberos
make %{_smp_mflags} LIBTOOL="$libtool"
popd

# Build 2.2.
build() {
%configure \
	--disable-slapd --disable-slurpd \
	--with-threads=posix --enable-static --enable-shared --enable-dynamic \
	\
	--enable-local --enable-rlookups \
	\
	--with-tls \
	--with-cyrus-sasl \
	\
	--enable-wrappers \
	\
	--enable-passwd \
	\
	--enable-cleartext \
	--enable-crypt \
	--enable-spasswd \
	--enable-modules \
	--disable-sql \
	\
	--libexecdir=%{_sbindir} \
	$@
make %{_smp_mflags} LIBTOOL="$libtool"
}

# Build the servers with Kerberos support (for password checking, mainly).
LIBS=-lpthread; export LIBS
pushd openldap-%{version_22}/build-servers
build \
	--enable-plugins \
	--enable-slapd \
	--enable-slurpd \
	--enable-bdb \
	--enable-hdb \
	--enable-ldap \
	--enable-ldbm \
	--with-ldbm-api=%{ldbm_backend} \
	--enable-meta \
	--enable-monitor \
	--enable-null \
	--enable-shell \
	--enable-sql=mod \
	--disable-perl \
	--disable-shared \
	--disable-dynamic \
	--with-kerberos=k5only
unset LDFLAGS
unset LIBS
popd

# Build clients without Kerberos password-checking support, which is only
# useful in the server anyway, to avoid stray dependencies.
pushd openldap-%{version_22}/build-clients
build \
	--disable-slapd \
	--disable-slurpd \
	--enable-shared \
	--enable-dynamic \
	--enable-static \
	--without-kerberos \
	--with-cyrus-sasl \
	--with-pic
popd

# Build evolution-specific clients just as we would normal clients, except with
# a different installation directory in mind and no shared libraries.
pushd evo-openldap-%{version_22}
build \
	--disable-slapd \
	--disable-slurpd \
	--disable-shared \
	--disable-dynamic \
	--enable-static \
	--without-kerberos \
	--with-cyrus-sasl \
	--with-pic \
	--includedir=%{evolution_connector_includedir} \
	--libdir=%{evolution_connector_libdir}
popd

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
libtool='%{_bindir}/libtool'
tagname=CC; export tagname

# Install the 2.0 server tools for dumping out old on-disk databases.
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}/
pushd openldap-%{version_20}
	pushd build-gdbm/servers/slapd/tools
	for bin in slapadd slapcat ; do
		../../../libtool --mode=install install -m755 $bin $RPM_BUILD_ROOT/%{_sbindir}/$bin-slapd-2.0-gdbm
	done
	popd

	pushd build-db/servers/slapd/tools
	for bin in slapadd slapcat ; do
		../../../libtool --mode=install install -m755 $bin $RPM_BUILD_ROOT/%{_sbindir}/$bin-slapd-2.0-dbb
	done
	popd
popd

# Install the 2.0 or 2.1 shared libraries for compatibility.  The two sets of
# libraries share sonames, so we have to choose one.
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/
pushd openldap-%{compat_version}/build-compat/libraries
	for lib in libldap libldap_r liblber ; do
		pushd $lib
		../../libtool --mode=install install -m755 $lib.la $RPM_BUILD_ROOT/%{_libdir}/$lib.la
		popd
	done
popd

# Install the 2.1 server tools for dumping out old on-disk databases.
pushd openldap-%{version_21}/build-servers/servers/slapd/tools
	for bin in slapadd slapcat ; do
		../../../libtool --mode=install install -m755 $bin $RPM_BUILD_ROOT/%{_sbindir}/$bin-slapd-2.1
	done
popd

# Install servers.
%ifarch %{nptl_arches}
case %{_target_platform} in
	i386*|i486*) archp=i486; arches="i586 i686";;
	i586*) archp=i586; arches=i686;;
	i686*) archp=i686; arches=;;
	athlon*) archp=i686; arches=;;
	*) archp=; arches=;;
esac

pushd db-instroot/%{_lib}/tls/
install -d $RPM_BUILD_ROOT/%{_libdir}/tls/${archp}/
install -m755 libslapd_db-*.*.so $RPM_BUILD_ROOT/%{_libdir}/tls/${archp}/
for arch in $arches ; do
	install -d $RPM_BUILD_ROOT/%{_libdir}/tls/${arch}/
	ln $RPM_BUILD_ROOT/%{_libdir}/tls/${archp}/* $RPM_BUILD_ROOT/%{_libdir}/tls/${arch}/
done
popd
%endif

pushd db-instroot/%{_lib}/
install -d $RPM_BUILD_ROOT/%{_libdir}/
install -m755 libslapd_db-*.*.so $RPM_BUILD_ROOT/%{_libdir}/
popd

pushd openldap-%{version_22}/build-servers
make install DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} LIBTOOL="$libtool"
popd

# Install the bdb maintenance tools.
pushd db-instroot/bin
for binary in db_* ; do
	install -m755 ${binary} $RPM_BUILD_ROOT/%{_sbindir}/slapd_${binary}
done
popd

# Install clients and shared libraries.  Install the evo-specific versions
# first so that any conflicting files are overwritten by generic versions.
pushd evo-openldap-%{version_22}
make install DESTDIR=$RPM_BUILD_ROOT \
	includedir=%{evolution_connector_includedir} \
	libdir=%{evolution_connector_libdir} \
	LIBTOOL="$libtool"
install -m644 \
	$RPM_SOURCE_DIR/README.evolution \
	$RPM_BUILD_ROOT/%{evolution_connector_prefix}/
popd
pushd openldap-%{version_22}/build-clients
make install DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} LIBTOOL="$libtool"
popd

# Create this directory so that authconfig setting TLS_CACERT to
# /etc/openldap/cacerts doesn't cause TLS startup of any kind to fail
# when the directory doesn't exist.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/openldap/cacerts


# Install the padl.com migration tools.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/openldap/migration
install -m 755 MigrationTools-%{migtools_version}/migrate_* \
	$RPM_BUILD_ROOT%{_datadir}/openldap/migration/
install -m 644 MigrationTools-%{migtools_version}/README \
	$RPM_SOURCE_DIR/migration-tools.txt \
	$RPM_BUILD_ROOT%{_datadir}/openldap/migration/
cp MigrationTools-%{migtools_version}/README README.migration
cp $RPM_SOURCE_DIR/migration-tools.txt TOOLS.migration

# Create the data directory.
mkdir -p $RPM_BUILD_ROOT/var/lib/ldap

# Hack the build root out of the default config files.
perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT/%{_sysconfdir}/openldap/*.conf

# Get the buildroot out of the man pages.
perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/*/*.*

# We don't need the default files -- RPM handles changes.
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/openldap/*.default
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/openldap/schema/*.default

# Install an init script for the servers.
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 $RPM_SOURCE_DIR/ldap.init $RPM_BUILD_ROOT/etc/rc.d/init.d/ldap

# If ldapadd and ldapmodify are the same binary, make them a hard link
if cmp $RPM_BUILD_ROOT%{_bindir}/ldapadd $RPM_BUILD_ROOT%{_bindir}/ldapmodify ; then
	ln -f $RPM_BUILD_ROOT%{_bindir}/ldapadd $RPM_BUILD_ROOT%{_bindir}/ldapmodify
fi

# Add some more schema for the sake of migration scripts.
install -d -m755 $RPM_BUILD_ROOT%{_sysconfdir}/openldap/schema/redhat
install -m644 \
	$RPM_SOURCE_DIR/autofs.schema \
	$RPM_BUILD_ROOT%{_sysconfdir}/openldap/schema/redhat/

# Tweak permissions on the libraries to make sure they're correct.
chmod 755 $RPM_BUILD_ROOT/%{_libdir}/lib*.so*
chmod 644 $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

# Remove files which we don't want packaged.
rm -f $RPM_BUILD_ROOT/%{_datadir}/openldap/migration/*.{instdir,simple,schema,mktemp,suffix}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{evolution_connector_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{evolution_connector_libdir}/*.so*
rm -f $RPM_BUILD_ROOT/%{_sbindir}/openldap/*.a
rm -f $RPM_BUILD_ROOT/%{_sbindir}/openldap/*.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%pre servers
# Take care to only do ownership-changing if we're adding the user.
if /usr/sbin/useradd -c "LDAP User" -u 55 \
	-s /bin/false -r -d /var/lib/ldap ldap 2> /dev/null ; then
	if [ -d /var/lib/ldap ] ; then
		for dbfile in /var/lib/ldap/* ; do
			if [ -f $dbfile ] ; then
				chown ldap:ldap $dbfile
			fi
		done
	fi
fi

%post servers
/sbin/ldconfig
/sbin/chkconfig --add ldap
exec > /dev/null 2> /dev/null
if [ ! -f %{_datadir}/ssl/certs/slapd.pem ] ; then
pushd %{_datadir}/ssl/certs
umask 077
cat << EOF | make slapd.pem
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF
chown root:ldap slapd.pem
chmod 640 slapd.pem
popd
fi
exit 0

%preun servers
if [ "$1" = "0" ] ; then
	/sbin/service ldap stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del ldap
fi

%postun servers
/sbin/ldconfig
if [ $1 -ge 1 ] ; then
	/sbin/service ldap condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%doc openldap-%{version_22}/ANNOUNCEMENT
%doc openldap-%{version_22}/CHANGES
%doc openldap-%{version_22}/COPYRIGHT
%doc openldap-%{version_22}/LICENSE
%doc openldap-%{version_22}/README
%attr(0755,root,root) %dir /etc/openldap
%attr(0755,root,root) %dir /etc/openldap/cacerts
%attr(0644,root,root) %config(noreplace) /etc/openldap/ldap*.conf
%attr(0755,root,root) %{_libdir}/liblber-*.so.*
%attr(0755,root,root) %{_libdir}/libldap-*.so.*
%attr(0755,root,root) %{_libdir}/libldap_r-*.so.*
%attr(0644,root,root) %{_mandir}/man5/ldif.5*
%attr(0644,root,root) %{_mandir}/man5/ldap.conf.5*
%attr(0755,root,root) %dir %{_datadir}/openldap

%files -n compat-openldap
%defattr(-,root,root)
%doc openldap-%{compat_version}/ANNOUNCEMENT
%doc openldap-%{compat_version}/COPYRIGHT
%doc openldap-%{compat_version}/LICENSE
%attr(0755,root,root) %{_libdir}/liblber.so.*
%attr(0755,root,root) %{_libdir}/libldap.so.*
%attr(0755,root,root) %{_libdir}/libldap_r.so.*

%files servers
%defattr(-,root,root)
%doc README.migration
%doc TOOLS.migration
%doc $RPM_SOURCE_DIR/README.upgrading $RPM_SOURCE_DIR/guide.html
%attr(0755,root,root) %config /etc/rc.d/init.d/ldap
%attr(0640,root,ldap) %config(noreplace) /etc/openldap/slapd.conf
%attr(0755,root,root) %dir /etc/openldap/schema
%attr(0644,root,root) %dir /etc/openldap/schema/README*
%attr(0644,root,root) %config(noreplace) /etc/openldap/schema/*.schema*
%attr(0755,root,root) %dir /etc/openldap/schema/redhat
%attr(0644,root,root) %config(noreplace) /etc/openldap/schema/redhat/*.schema*
%attr(0755,root,root) %{_sbindir}/sl*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0644,root,root) %{_mandir}/man5/slapd*.5*
%attr(0755,root,root) %dir %{_datadir}/openldap/migration
%attr(0644,root,root) %{_datadir}/openldap/migration/README
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/migration/*.ph
%attr(0755,root,root) %{_datadir}/openldap/migration/*.pl
%attr(0755,root,root) %{_datadir}/openldap/migration/*.sh
%attr(0644,root,root) %{_datadir}/openldap/migration/*.txt
%attr(0755,root,root) %dir %{_datadir}/openldap/ucdata
%attr(0644,root,root) %dir %{_datadir}/openldap/ucdata/*
%attr(0700,ldap,ldap) %dir /var/lib/ldap
%attr(0755,root,root) %{_libdir}/libslapd_db-*.*.so
%ifarch %{nptl_arches}
%attr(0755,root,root) %{_libdir}/tls
%endif

%files servers-sql
%defattr(-,root,root)
%doc openldap-%{version_22}/servers/slapd/back-sql/docs/*
%doc openldap-%{version_22}/servers/slapd/back-sql/rdbms_depend
%attr(0755,root,root) %{_sbindir}/openldap/back_sql.la
%attr(0755,root,root) %{_sbindir}/openldap/back_sql*.so.*

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%doc openldap-%{version_22}/doc/drafts openldap-%{version_22}/doc/rfc
%attr(0755,root,root) %{_libdir}/libl*.so
%attr(0644,root,root) %{_libdir}/libl*.a
%attr(0644,root,root) %{_includedir}/*
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0755,root,root) %dir %{evolution_connector_prefix}
%attr(0644,root,root)      %{evolution_connector_prefix}/README*
%attr(0755,root,root) %dir %{evolution_connector_includedir}
%attr(0644,root,root)      %{evolution_connector_includedir}/*.h
%attr(0755,root,root) %dir %{evolution_connector_libdir}
%attr(0644,root,root)      %{evolution_connector_libdir}/*.a

%changelog
* Mon Apr 24 2006 Jay Fenlason <fenlason@redhat.com> 2.2.13-6.4E
- Change autofs.schema to use the correct OID for the automount objectlass.
  This closes bz#150340 OID conflict in LDAP schemas shipped
- Double the thread stack size on ia64 to close
  bz#176602 ? [RHEL4] slapd on ia64 seg faults and dies whenever ldapsearch is run against it.
- Include the gethostbyname_r patch to close
  bz#186095 use gethostbyname_r() instead of gethostbyname() in ldap_init()

* Thu Apr 13 2006 Jay Fenlason <fenlason@redhat.com> 2.2.13-5.4E
- Include the wait4msg-select-fix patch from Jeffery Layton
  <jlayton@redhat.com> (backported from 2.2.29) to close
  bz#186447 ldapsearch hangs when using SSL with Active Directory as LDAP Server

* Tue Mar 21 2006 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-4.2
- rebuild, using the system copy of libtool for the compat libraries (#183331)

* Tue Mar 21 2006 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-4.1
- rebuild

* Sat Jan 28 2006 Vince Worthington <vincew@redhat.com>
- Patch all Makefile.in's that still had "-s" as an install argument in
  make install targets for binaries like slapd and client tools, so
  find-debuginfo.sh gets a chance to extract the debug symbols for 
  -debuginfo RPM (BZ#163070).

* Thu Aug 11 2005 Jay Fenlason <fenlason@redhat.com> 2.2.13-3.4E
- Backport the -hop patches to prevent infinite looping when chasing referrals.
  OpenLDAP ITS #3578 as described in
  bz#158120 [RHEL3] Need help configuring host as an LDAP client

- Create and own the /etc/openldap/cacerts directory, to close
  bz#159151 Authconfig update creates a problem with OpenLDAP server

* Tue Jul 5 2005 Jay Fenlason <fenlason@redhat.com>
- Include fix for
  bz#161990 openldap password disclosure issue

* Tue Apr 19 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-3
- move nptl libraries into arch-specific subdirectories on %%{ix86} boxes,
  to match glibc's layout
- update notes on upgrading from previous releases
- pull in fix for ITS #3201 from 2.2.15
- pull in fix for ITS #3326 from 2.2.16

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-2
- build a separate, static set of libraries for openldap-devel with the
  non-standard ntlm bind patch applied, for use by the evolution-connector
  package (#125579), and installing them under
  %%{evolution_connector_prefix} (%{evolution_connector_prefix})
- provide openldap-evolution-devel = %%{version}-%%{release} in openldap-devel
  so that evolution-connector's source package can require a version of
  openldap-devel which provides what it wants

* Mon Jul 26 2004 Nalin Dahyabhai <nalin@redhat.com>
- update administrator guide

* Wed Jun 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-1
- add compat-openldap subpackage
- default to bdb, as upstream does, gambling that we're only going to be
  on systems with nptl now

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-0
- preliminary 2.2.13 update
- move ucdata to the -servers subpackage where it belongs

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-1
- build experimental sql backend as a loadable module

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-0
- update to 2.1.30

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.1.29-3
- removed rpath
- added pie patch: slapd and slurpd are now pie
- requires libtool >= 1.5.6-2 (PIC libltdl.a)

* Fri Apr 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-2
- move rfc documentation from main to -devel (#121025)

* Wed Apr 14 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-1
- rebuild

* Tue Apr  6 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-0
- update to 2.1.29 (stable 20040329)

* Mon Mar 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- don't build servers with --with-kpasswd, that option hasn't been recognized
  since 2.1.23

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 2.1.25-5.1
- rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 2.1.25-5
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-4
- remove 'reload' from the init script -- it never worked as intended (#115310)

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-3
- commit that last fix correctly this time

* Tue Feb  3 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-2
- fix incorrect use of find when attempting to detect a common permissions
  error in the init script (#114866)

* Fri Jan 16 2004 Nalin Dahyabhai <nalin@redhat.com>
- add bug fix patch for DB 4.2.52

* Thu Jan  8 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-1
- change logging facility used from daemon to local4 (#112730, reversing #11047)
  BEHAVIOR CHANGE - SHOULD BE MENTIONED IN THE RELEASE NOTES.

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fix for logic quasi-bug in slapd's SASL auxprop code (Dave Jones)

* Thu Dec 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.25, now marked STABLE

* Thu Dec 11 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-9
- update to db-4.2.52.

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-8
- add another section to the ABI note for the TLS libdb so that it's marked as
  not needing an executable stack (from Arjan Van de Ven)

* Thu Oct 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-7
- force bundled libdb to not use O_DIRECT by making it forget that we have it

* Wed Oct 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- build bundled libdb for slapd dynamically to make the package smaller,
  among other things
- on tls-capable arches, build libdb both with and without shared posix
  mutexes, otherwise just without
- disable posix mutexes unconditionally for db 4.0, which shouldn't need
  them for the migration cases where it's used
- update to MigrationTools 45

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-6.1
- upgrade db-4.1.25 to db-4.2.42.

* Fri Sep 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-6
- drop rfc822-MailMember.schema, merged into upstream misc.schema at some point

* Wed Aug 27 2003 Nalin Dahyabhai <nalin@redhat.com>
- actually require newer libtool, as was intended back in 2.1.22-0, noted as
  missed by Jim Richardson

* Fri Jul 25 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-5
- enable rlookups, they don't cost anything unless also enabled in slapd's
  configuration file

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-4
- rebuild

* Thu Jul 17 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-3
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-2
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-1
- build

* Mon Jul 14 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-0
- 2.1.22 now badged stable
- be more aggressive in what we index by default
- use/require libtool 1.5

* Mon Jun 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.22

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-1
- update to 2.1.21
- enable ldap, meta, monitor, null, rewrite in slapd

* Mon May 19 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-1
- update to 2.1.20

* Thu May  8 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-1
- update to 2.1.19

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-1
- switch to db with crypto

* Fri May  2 2003 Nalin Dahyabhai <nalin@redhat.com>
- install the db utils for the bundled libdb as %%{_sbindir}/slapd_db_*
- install slapcat/slapadd from 2.0.x for migration purposes

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.17
- disable the shell backend, not expected to work well with threads
- drop the kerberosSecurityObject schema, the krbName attribute it
  contains is only used if slapd is built with v2 kbind support

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-8
- back down to db 4.0.x, which 2.0.x can compile with in ldbm-over-db setups
- tweak SuSE patch to fix a few copy-paste errors and a NULL dereference

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-6
- rebuild

* Mon Dec 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-5
- rebuild

* Fri Dec 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-4
- check for setgid as well

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-3
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fixes from SuSE's security audit, except for fixes to ITS 1963,
  1936, 2007, 2009, which were included in 2.0.26.
- add two more patches for db 4.1.24 from sleepycat's updates page
- use openssl pkgconfig data, if any is available

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-2
- add patches for db 4.1.24 from sleepycat's updates page

* Mon Nov  4 2002 Nalin Dahyabhai <nalin@redhat.com>
- add a sample TLSCACertificateFile directive to the default slapd.conf

* Tue Sep 24 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-1
- update to 2.0.27

* Fri Sep 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.26-1
- update to 2.0.26, db 4.1.24.NC

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-2
- change LD_FLAGS to refer to %{_prefix}/kerberos/%{_lib} instead of
  /usr/kerberos/lib, which might not be right on some arches

* Mon Aug 26 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-1
- update to 2.0.25 "stable", ldbm-over-gdbm (putting off migration of LDBM
  slapd databases until we move to 2.1.x)
- use %%{_smp_mflags} when running make
- update to MigrationTools 44
- enable dynamic module support in slapd

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-5
- rebuild in new environment

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-3
- use the gdbm backend again

* Mon Feb 18 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-2
- make slapd.conf read/write by root, read by ldap

* Sun Feb 17 2002 Nalin Dahyabhai <nalin@redhat.com>
- fix corner case in sendbuf fix
- 2.0.23 now marked "stable"

* Tue Feb 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-1
- update to 2.0.23

* Fri Feb  8 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-2
- switch to an internalized Berkeley DB as the ldbm back-end  (NOTE: this breaks
  access to existing on-disk directory data)
- add slapcat/slapadd with gdbm for migration purposes
- remove Kerberos dependency in client libs (the direct Kerberos dependency
  is used by the server for checking {kerberos} passwords)

* Fri Feb  1 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-1
- update to 2.0.22

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de> 2.0.21-5
- prereq chkconfig for server subpackage

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-4
- update migration tools to version 40

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-3
- free ride through the build system

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-2
- update to 2.0.21, now earmarked as STABLE

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-2
- temporarily disable optimizations for ia64 arches
- specify pthreads at configure-time instead of letting configure guess

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com>
- and one for Raw Hide

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-0.7
- build for RHL 7/7.1

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-1
- update to 2.0.20 (security errata)

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.19-1
- update to 2.0.19

* Wed Nov  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-2
- fix the commented-out replication example in slapd.conf

* Fri Oct 26 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-1
- update to 2.0.18

* Mon Oct 15 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.17-1
- update to 2.0.17

* Wed Oct 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable kbind support (deprecated, and I suspect unused)
- configure with --with-kerberos=k5only instead of --with-kerberos=k5
- build slapd with threads

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-2
- rebuild, 2.0.15 is now designated stable

* Fri Sep 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-1
- update to 2.0.15

* Mon Sep 10 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.14-1
- update to 2.0.14

* Fri Aug 31 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.12-1
- update to 2.0.12 to pull in fixes for setting of default TLS options, among
  other things
- update to migration tools 39
- drop tls patch, which was fixed better in this release

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.11-13
- install saucer correctly

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to fix ldap_set_options not being able to set global options related
  to TLS correctly

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't attempt to create a cert at install-time, it's usually going
  to get the wrong CN (#51352)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a build-time requirement on pam-devel
- add a build-time requirement on a sufficiently-new libtool to link
  shared libraries to other shared libraries (which is needed in order
  for prelinking to work)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- require cyrus-sasl-md5 (support for DIGEST-MD5 is required for RFC
  compliance) by name (follows from #43079, which split cyrus-sasl's
  cram-md5 and digest-md5 modules out into cyrus-sasl-md5)

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable passwd back-end (noted by Alan Sparks and Sergio Kessler)

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- start to prep for errata release

* Fri Jul  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- link libldap with liblber

* Wed Jul  4 2001 Than Ngo <than@redhat.com> 2.0.11-6
- add symlink liblber.so libldap.so and libldap_r.so in /usr/lib

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move shared libraries to /lib
- redo init script for better internationalization (#26154)
- don't use ldaprc files in the current directory (#38402) (patch from
  hps@intermeta.de)
- add BuildPrereq on tcp wrappers since we configure with
  --enable-wrappers (#43707)
- don't overflow debug buffer in mail500 (#41751)
- don't call krb5_free_creds instead of krb5_free_cred_contents any
  more (#43159)

* Mon Jul  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- make config files noreplace (#42831)

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually change the default config to use the dummy cert
- update to MigrationTools 38

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- build dummy certificate in %%post, use it in default config
- configure-time shenanigans to help a confused configure script

* Wed Jun 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak migrate_automount and friends so that they can be run from anywhere

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.11

* Wed May 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.10

* Mon May 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.9

* Tue May 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.8
- drop patch which came from upstream

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- back out pidfile patches, which interact weirdly with Linux threads
- mark non-standard schema as such by moving them to a different directory

* Mon Feb  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to MigrationTools 36, adds netgroup support

* Fri Jan 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix thinko in that last patch

* Thu Jan 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to work around some buffering problems

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Fri Jan 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- move the RFCs to the base package (#21701)
- update to MigrationTools 34

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- add support for additional OPTIONS, SLAPD_OPTIONS, and SLURPD_OPTIONS in
  a /etc/sysconfig/ldap file (#23549)

* Fri Dec 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object OID from 1.3.6.1.1.1.2.9 to 1.3.6.1.1.1.2.13,
  per mail from the ldap-nis mailing list

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- force -fPIC so that shared libraries don't fall over

* Mon Dec  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Norbert Klasen's patch (via Del) to fix searches using ldaps URLs
  (OpenLDAP ITS #889)
- add "-h ldaps:///" to server init when TLS is enabled, in order to support
  ldaps in addition to the regular STARTTLS (suggested by Del)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- correct mismatched-dn-cn bug in migrate_automount.pl

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to the correct OIDs for automount and automountInformation
- add notes on upgrading

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.7
- drop chdir patch (went mainstream)

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object classes from auxiliary to structural

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to Migration Tools 27
- change the sense of the last simple patch

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- reorganize the patch list to separate MigrationTools and OpenLDAP patches
- switch to Luke Howard's rfc822MailMember schema instead of the aliases.schema
- configure slapd to run as the non-root user "ldap" (#19370)
- chdir() before chroot() (we don't use chroot, though) (#19369)
- disable saving of the pid file because the parent thread which saves it and
  the child thread which listens have different pids

* Wed Oct 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add missing required attributes to conversion scripts to comply with schema
- add schema for mail aliases, autofs, and kerberosSecurityObject rooted in
  our own OID tree to define attributes and classes migration scripts expect
- tweak automounter migration script

* Mon Oct  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- try adding the suffix first when doing online migrations
- force ldapadd to use simple authentication in migration scripts
- add indexing of a few attributes to the default configuration
- add commented-out section on using TLS to default configuration

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.6
- add buildprereq on cyrus-sasl-devel, krb5-devel, openssl-devel
- take the -s flag off of slapadd invocations in migration tools
- add the cosine.schema to the default server config, needed by inetorgperson

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the nis.schema and inetorgperson.schema to the default server config
- make ldapadd a hard link to ldapmodify because they're identical binaries

* Fri Sep 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.4

* Fri Sep 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove prereq on /etc/init.d (#17531)
- update to 2.0.3
- add saucer to the included clients

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.1

* Fri Sep  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.0
- patch to build against MIT Kerberos 1.1 and later instead of 1.0.x

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove that pesky default password
- change "Copyright:" to "License:"

* Sun Aug 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- adjust permissions in files lists
- move libexecdir from %%{_prefix}/sbin to %%{_sbindir}

* Fri Aug 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add migrate_automount.pl to the migration scripts set

* Tue Aug  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- build a semistatic slurpd with threads, everything else without
- disable reverse lookups, per email on OpenLDAP mailing lists
- make sure the execute bits are set on the shared libraries

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- change logging facility used from local4 to daemon (#11047)

* Thu Jul 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- split off clients and servers to shrink down the package and remove the
  base package's dependency on Perl
- make certain that the binaries have sane permissions

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the init script back

* Thu Jul 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the init script to only source /etc/sysconfig/network if it's found

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch to gdbm; I'm getting off the db merry-go-round
- tweak the init script some more
- add instdir to @INC in migration scripts

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak init script to return error codes properly
- change initscripts dependency to one on /etc/init.d

* Tue Jul  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- prereq initscripts
- make migration scripts use mktemp

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- do condrestart in post and stop in preun
- move init script to /etc/init.d

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.11
- add condrestart logic to init script
- munge migration scripts so that you don't have to be
  /usr/share/openldap/migration to run them
- add code to create pid files in /var/run

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS tweaks
- fix for compiling with libdb2

* Thu May  4 2000 Bill Nottingham <notting@redhat.com>
- minor tweak so it builds on ia64

* Wed May  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- more minimalistic fix for bug #11111 after consultation with OpenLDAP team
- backport replacement for the ldapuser patch

* Tue May  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix segfaults from queries with commas in them in in.xfingerd (bug #11111)

* Tue Apr 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.10
- add revamped version of patch from kos@bastard.net to allow execution as
  any non-root user
- remove test suite from %%build because of weirdness in the build system

* Wed Apr 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the defaults for databases and whatnot to /var/lib/ldap (bug #10714)
- fix some possible string-handling problems

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- start earlier, stop later.

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- auto rebuild in new environment (release 4)

* Tue Feb  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add -D_REENTRANT to make threaded stuff more stable, even though it looks
  like the sources define it, too
- mark *.ph files in migration tools as config files

* Fri Jan 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.9

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip files

* Sat Sep 11 1999 Bill Nottingham <notting@redhat.com>
- update to 1.2.7
- fix some bugs from bugzilla (#4885, #4887, #4888, #4967)
- take include files out of base package

* Fri Aug 27 1999 Jeff Johnson <jbj@redhat.com>
- missing ;; in init script reload) (#4734).

* Tue Aug 24 1999 Cristian Gafton <gafton@redhat.com>
- move stuff from /usr/libexec to /usr/sbin
- relocate config dirs to /etc/openldap

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- add the migration tools to the package

* Fri Aug 06 1999 Cristian Gafton <gafton@redhat.com>
- upgrade to 1.2.6
- add rc.d script
- split -devel package

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to latest stable (1.1.4), it now uses configure macro.

* Fri Jan 15 1999 Bill Nottingham <notting@redhat.com>
- build on arm, glibc2.1

* Wed Oct 28 1998 Preston Brown <pbrown@redhat.com>
- initial cut.
- patches for signal handling on the alpha
