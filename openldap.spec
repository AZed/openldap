%define migtools_ver 44
%define db_version 4.0.14

# For RHL 7.x, 8.0, RHEL 2.1, we use "gdbm" (.gdbm).
# For RHL 9, RHEL 3, we use "berkeley" (.dbb).
%define ldbm_backend berkeley

%define nss_ldap_prefix %{_libdir}/nss_ldap-openldap
%define nss_ldap_includedir %{nss_ldap_prefix}/include
%define nss_ldap_libdir %{nss_ldap_prefix}/%{_lib}

Summary: The configuration files, libraries, and documentation for OpenLDAP.
Name: openldap
Version: 2.0.27
Release: 23
License: OpenLDAP
Group: System Environment/Daemons
Source0: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1: http://www.sleepycat.com/update/%{db_version}/db-%{db_version}.tar.gz
Source2: ldap.init
Source3: ftp://ftp.padl.com/pub/MigrationTools-%{migtools_ver}.tar.gz
Source4: migration-tools.txt
Source6: autofs.schema
Source7: kerberosobject.schema
Source8: README.upgrading
Source9: README.sendbuf
Source10: http://www.OpenLDAP.org/doc/admin/guide.html
Patch0: openldap-2.0.16-config.patch
Patch1: openldap-2.0.12-redhat.patch
Patch2: openldap-1.2.11-cldap.patch
Patch3: openldap-2.0.3-syslog.patch
Patch6: openldap-2.0.23-sendbuf.patch
Patch7: openldap-2.0.11-ldaprc.patch
Patch8: openldap-2.0.11-debug.patch
Patch9: openldap-2.0.11-libtool.patch
Patch10: openldap-2.0.11-linkage.patch
Patch21: MigrationTools-38-instdir.patch
Patch22: MigrationTools-36-mktemp.patch
Patch23: MigrationTools-27-simple.patch
Patch24: MigrationTools-26-suffix.patch
Patch25: MigrationTools-44-schema.patch
Patch26: openldap-2.0.27-susesec.patch
Patch27: openldap-2.0.27-messages-references.patch
Patch28: openldap-2.0.27-openssl-0.9.7.patch
Patch29: openldap-2.0.27-hostnamecheck.patch
Patch30: openldap-2.0.27-64.patch
Patch31: openldap-2.0.27-hop.patch
Patch32: openldap-2.0.27-start_tls-async.patch
Patch33: openldap-2.0.27-lutil-passwd.patch
Patch34: openldap-2.2.13-tls-fix-connection-test.patch
Patch35: openldap-2.0.27-tls-cache.patch
Patch36: openldap-2.0.27-hang.patch
Patch37: openldap-2.0.27-selfwrite.patch
Patch38: openldap-2.0.27-start_tls-leak.patch
Patch39: openldap-2.0.27-ppc64.patch
URL: http://www.openldap.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildPreReq: cyrus-sasl-devel, gdbm-devel, krb5-devel, openssl-devel
BuildPreReq: pam-devel, perl, pkgconfig, tcp_wrappers, readline-devel
BuildPreReq: libtool >= 1.4
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
Requires: openldap = %{version}-%{release}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package servers
Summary: OpenLDAP servers and related files.
Prereq: fileutils, make, openldap = %{version}-%{release}, openssl, /usr/sbin/useradd, /sbin/chkconfig
Group: System Environment/Daemons

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd and slurpd servers,
migration scripts, and related files.

%package clients
Summary: Client programs for OpenLDAP.
Prereq: openldap = %{version}-%{release}
Group: Applications/Internet

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.

%prep
%setup -q -a 1 -a 3 -c

pushd MigrationTools-%{migtools_ver}
%patch21 -p1 -b .instdir
%patch22 -p1 -b .mktemp
%patch23 -p1 -b .simple
%patch24 -p1 -b .suffix
%patch25 -p1 -b .schema
popd

pushd %{name}-%{version}
%patch0 -p1 -b .config
%patch1 -p1 -b .redhat
%patch2 -p1 -b .cldap
%patch3 -p1 -b .syslog
%patch6 -p1 -b .sendbuf
%patch7 -p1 -b .ldaprc
%patch8 -p1 -b .debug
%patch9 -p1 -b .libtool
%patch10 -p1 -b .linkage
%patch26 -p0 -b .susesec
%patch27 -p1 -b .messages-references
%patch28 -p1 -b .openssl-0.9.7
%patch29 -p1 -b .hostnamecheck
%patch30 -p1 -b .64
%patch31 -p1 -b .hop
%patch33 -p1 -b .lutil-passwd
%patch34 -p1 -b .CAN-2005-2069
%patch35 -p1 -b .tls-cache
%patch36 -p1 -b .hang
%patch37 -p1 -b .selfwrite
%patch38 -p1 -b .start_tls-leak
%patch39 -p1 -b .ppc64
cp %{_datadir}/libtool/config.{sub,guess} build/
popd

cp -a %{name}-%{version} %{name}-%{version}-build-nss_ldap

pushd %{name}-%{version}
mkdir build-gdbm
ln -s ../configure build-gdbm
mkdir build-berkeley
ln -s ../configure build-berkeley
mkdir build-krb5
ln -s ../configure build-krb5
mkdir build-clients
ln -s ../configure build-clients
popd

pushd %{name}-%{version}-build-nss_ldap
%patch32 -p0 -b .start_tls
mkdir build-clients
ln -s ../configure build-clients
popd

%build
dbdir=`pwd`/db-instroot
%ifarch ia64
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -O0"
%endif
if pkg-config openssl ; then
	OPENSSL_CPPFLAGS=`pkg-config --cflags openssl`
	CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
	OPENSSL_LDFLAGS=`pkg-config --libs-only-L openssl`
	LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS
fi
CFLAGS="$CPPFLAGS $RPM_OPT_FLAGS -D_REENTRANT -fPIC"; export CFLAGS
TARGET_PLATFORM=%{_target_platform}
%define _target_platform --target=${TARGET_PLATFORM}
build() {
cat << _EOF | sed -e 's,--host=[^ ]*,,g' -e 's,--build=[^ ]*,,g' -e 's,--target=[^ ]*,,g' -e 's,%{_target_platform},,g' > run-build
%configure \
	--with-slapd --with-slurpd --without-ldapd \
	--with-threads=posix --enable-static \
	\
	--enable-local --enable-cldap --disable-rlookups \
	\
	--with-tls \
	--with-cyrus-sasl \
	\
	--enable-wrappers \
	\
	--enable-passwd \
	--enable-shell \
	--enable-cleartext \
	--enable-crypt \
	--enable-spasswd \
	--enable-modules \
	--disable-sql \
	\
	--libexecdir=%{_sbindir} \
	--localstatedir=/%{_var}/run \
	$@ \$@
_EOF
sh -x ./run-build %{_target_platform}
make depend %{_smp_mflags}
make %{_smp_mflags}
}
# Build Berkeley DB and install it into a temporary area, isolating OpenLDAP
# from any future changes to the system-wide Berkeley DB library.
pushd db-%{db_version}/dist
./configure --with-pic --disable-shared --with-uniquename=_openldap_rhl --prefix=${dbdir} --libdir=${dbdir}/%{_lib}
make %{_smp_mflags}
make install
popd
# Build one for tools which use gdbm.
CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS
pushd %{name}-%{version}/build-gdbm
build --enable-ldbm --with-ldbm-api=gdbm --disable-shared --without-kerberos
popd
# Build one for tools which use db.
CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS
LIBS="-lpthread"; export LIBS
CPPFLAGS="$CPPFLAGS -I${dbdir}/include"
LDFLAGS="$LDFLAGS -L${dbdir}/%{_lib}"
pushd %{name}-%{version}/build-berkeley
build --enable-ldbm --with-ldbm-api=berkeley --disable-shared --without-kerberos
popd
# Build the servers with Kerberos support and whichever backend we want.  Even
# enable the bdb backend, which doesn't exist yet.
CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS
LIBS="-lpthread"; export LIBS
pushd %{name}-%{version}/build-krb5
CPPFLAGS="$CPPFLAGS -I${dbdir}/include -I%{_prefix}/kerberos/include -DHAVE_KERBEROS_V"
LDFLAGS="$LDFLAGS -L${dbdir}/%{_lib} -L%{_prefix}/kerberos/%{_lib}"
build --enable-ldbm --with-ldbm-api=%{ldbm_backend} --enable-bdb --disable-shared --with-kerberos=k5only --enable-kpasswd
popd
# Build clients without Kerberos password-checking support, which is only
# useful in the server anyway.
CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS
unset LIBS
pushd %{name}-%{version}/build-clients
build --disable-ldbm --enable-shared --without-kerberos
popd
pushd %{name}-%{version}-build-nss_ldap/build-clients
build --disable-ldbm --enable-shared --without-kerberos --includedir=%{nss_ldap_includedir} --libdir=%{nss_ldap_libdir}
popd

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
makeinstall() {
%makeinstall \
	datadir=$RPM_BUILD_ROOT%{_datadir}/openldap \
	libexecdir=$RPM_BUILD_ROOT%{_sbindir} \
	localstatedir=/%{_var}/run \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}/openldap $@
}

# Install compatibility binaries.
pushd %{name}-%{version}/build-gdbm
makeinstall -C servers/slapd/tools
mv $RPM_BUILD_ROOT%{_sbindir}/slapadd $RPM_BUILD_ROOT%{_sbindir}/slapadd-gdbm
mv $RPM_BUILD_ROOT%{_sbindir}/slapcat $RPM_BUILD_ROOT%{_sbindir}/slapcat-gdbm
popd
if [ %{ldbm_backend} != gdbm ] ; then
	pushd %{name}-%{version}/build-berkeley
	makeinstall -C servers/slapd/tools
	mv $RPM_BUILD_ROOT%{_sbindir}/slapadd $RPM_BUILD_ROOT%{_sbindir}/slapadd-berkeley
	mv $RPM_BUILD_ROOT%{_sbindir}/slapcat $RPM_BUILD_ROOT%{_sbindir}/slapcat-berkeley
	popd
fi

# Install clients and libraries.
pushd %{name}-%{version}/build-clients
makeinstall
popd

pushd %{name}-%{version}-build-nss_ldap/build-clients
makeinstall
popd

# Install servers with Kerberos support.
pushd %{name}-%{version}/build-krb5
makeinstall -C servers
popd

# Set the right set of slap... tools for the server.
ln -f $RPM_BUILD_ROOT%{_sbindir}/slapadd-%{ldbm_backend} $RPM_BUILD_ROOT%{_sbindir}/slapadd
ln -f $RPM_BUILD_ROOT%{_sbindir}/slapcat-%{ldbm_backend} $RPM_BUILD_ROOT%{_sbindir}/slapcat

# Install the padl.com migration tools.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/openldap/migration
install -m 755 MigrationTools-%{migtools_ver}/migrate_* \
	$RPM_BUILD_ROOT%{_datadir}/openldap/migration
install -m 644 MigrationTools-%{migtools_ver}/README %{SOURCE4} \
	$RPM_BUILD_ROOT%{_datadir}/openldap/migration
cp MigrationTools-%{migtools_ver}/README README.migration
cp %{SOURCE4} TOOLS.migration

# try to build saucer, but don't fret if we can't
pushd %{name}-%{version}/build-clients
if make -C contrib/saucer ; then
	./libtool install -m755 contrib/saucer/saucer $RPM_BUILD_ROOT/%{_bindir}/
	./libtool install -m644 ../contrib/saucer/saucer.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
fi
popd

# Create the data directory.
mkdir -p $RPM_BUILD_ROOT/var/lib/ldap

# Hack the build root out of the default config files.
perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT/%{_sysconfdir}/openldap/slapd.conf

# Get the buildroot out of the man pages.
perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/*/*.*

# We don't need the default files -- RPM handles changes.
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/openldap/*.default
#rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/openldap/schema/*.default

# Install an init script for the server.
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/ldap

# If ldapadd and ldapmodify are the same binary, make them a hard link
if cmp $RPM_BUILD_ROOT%{_bindir}/ldapadd $RPM_BUILD_ROOT%{_bindir}/ldapmodify ; then
	ln -f $RPM_BUILD_ROOT%{_bindir}/ldapadd $RPM_BUILD_ROOT%{_bindir}/ldapmodify
fi

# Add some more schema for the sake of migration scripts.
install -d -m755 $RPM_BUILD_ROOT%{_sysconfdir}/openldap/schema/redhat
install -m644 %{SOURCE6} %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/openldap/schema/redhat/

# Tweak permissions on the libraries to make sure they're correct.
chmod 755 $RPM_BUILD_ROOT/%{_libdir}/lib*.so*
chmod 644 $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

# Remove files we don't want packaged.
rm -f $RPM_BUILD_ROOT/%{_datadir}/openldap/migration/*.{instdir,simple,schema,mktemp,suffix}
rm -f $RPM_BUILD_ROOT/%{_datadir}/openldap/*-
rm -f $RPM_BUILD_ROOT/%{_bindir}/*-
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

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
				chown ldap.ldap $dbfile
			fi
		done
	fi
fi

%post servers
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
chown root.ldap slapd.pem
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
%doc %{name}-%{version}/{ANNOUNCEMENT,CHANGES,COPYRIGHT,LICENSE,README} %{name}-%{version}/doc/rfc
%attr(0755,root,root) %dir /etc/openldap
%attr(0644,root,root) %config(noreplace) /etc/openldap/ldap*.conf
%attr(0755,root,root) %{_libdir}/lib*.so.*
%attr(0644,root,root) %{_mandir}/man5/*
%attr(0755,root,root) %dir %{_datadir}/openldap
%attr(0644,root,root) %{_datadir}/openldap/ldapfriendly

%files servers
%defattr(-,root,root)
%doc README.migration TOOLS.migration
%doc $RPM_SOURCE_DIR/README.upgrading $RPM_SOURCE_DIR/README.sendbuf $RPM_SOURCE_DIR/guide.html
%attr(0755,root,root) %config /etc/rc.d/init.d/ldap
%attr(0640,root,ldap) %config(noreplace) /etc/openldap/slapd.conf
%attr(0755,root,root) %dir /etc/openldap/schema
%attr(0644,root,root) %config(noreplace) /etc/openldap/schema/*.schema*
%attr(0755,root,root) %dir /etc/openldap/schema/redhat
%attr(0644,root,root) %config(noreplace) /etc/openldap/schema/redhat/*.schema*
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0644,root,root) %{_datadir}/openldap/*.help
%attr(0755,root,root) %dir %{_datadir}/openldap/migration
%attr(0644,root,root) %{_datadir}/openldap/migration/README
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/migration/*.ph
%attr(0755,root,root) %{_datadir}/openldap/migration/*.pl
%attr(0755,root,root) %{_datadir}/openldap/migration/*.sh
%attr(0644,root,root) %{_datadir}/openldap/migration/*.txt
%attr(0700,ldap,ldap) %dir /var/lib/ldap

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%doc %{name}-%{version}/doc/drafts
%attr(0755,root,root) %{_libdir}/lib*.so
%attr(0644,root,root) %{_libdir}/lib*.a
%attr(0644,root,root) %{_includedir}/*
%attr(0644,root,root) %{_mandir}/man3/*

%changelog
* Wed Mar 28 2007 Jay Fenlason <fenlason@redhat.com> 2.0.27-23
- Include the -ppc64 patch to fix a ppc64-specific build failure.
- Put back smp_mflags

* Tue Mar 27 2007 Jay Fenlason <fenlason@redhat.com> 2.0.27-22
- remove smp_mflags to work around a build-time race condition
- backport the -selfwrite patch
  Resolves: rhbz#234222 CVE-2006-4600 openldap improper selfwrite access
- Include the start_tls-leak patch
  Resolves: rhbz#174830: ldap_start_tls_s() leaks

* Thu Mar 2 2006 Jay Fenlason <fenlason@redhat.com> 2.0.27-22
- Add -hang patch (backported from 2.2.13) to finish fixing
  bz#177570 SSL session caching causes client hangs when doing multiple
   connections

* Thu Jan 12 2006 Jay Fenlason <fenlason@redhat.com> 2.0.27-21
- Add -tls-cache.patch from upstream (rev 1.92 of
  /repo/OpenLDAP/pkg/ldap/libraries/libldap/tls.c,v) to close
  bz#177570 SSL session caching causes client hangs when doing multiple
   connections

* Fri Aug 19 2005 Jay Fenlason <fenlason@redhat.com> 2.0.27-20
- Fix packaging error that left usr/bin/ud- in the -clients rpm.
- Add readline-devel to BuildPreReq so that saucer always gets built.

* Tue Aug 9 2005 Jay Fenlason <fenlason@redhat.com> 2.0.27-19
- Backport tls-fix-connection-test patch (CAN-2005-2069) for
  bz#161990 openldap password disclosure issue

* Wed May  4 2005 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-18
- backport fix to hashed-passwords-can-be-treated-as-plaintext (CAN-2004-0823)
  (#156386)
- ITS #3578, stop chasing v3 referrals at some point

* Thu Sep  2 2004 Jonathan Blandford <jrb@redhat.com> 2.0.27-17
- Change ldbm_backend to berkeley.  Patch from Warren Togami.

* Fri Aug 27 2004 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-15
- incorporate fix for implicit declarations of some functions which return
  pointers

* Wed May 26 2004 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-14
- incorporate patch to perform SSL certificate name check if and only if
  the certificate is being validated (more of #111492)

* Tue May 18 2004 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-13
- incorporate fix for client crash when server certs include a subjectAltName
  field (#111492)

* Wed Mar 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-4.7
- rebuild

* Tue Feb 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-12
- remove 'reload' from the init script -- it never worked as intended (#115310)

* Fri Sep 19 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-11
- include messages.lo and references.lo in libldap_r (#104691)

* Fri Sep 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-10
- remove rfc822-MailMember.schema, contents merged into upstream misc.schema

* Tue Jun 17 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-9
- don't use the system libtool

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
