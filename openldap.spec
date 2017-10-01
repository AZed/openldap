# TODO: add make test after build

%define ldbm_backend berkeley
%define evolution_connector_prefix %{_libdir}/evolution-openldap
%define evolution_connector_includedir %{evolution_connector_prefix}/include
%define evolution_connector_libdir %{evolution_connector_prefix}/%{_lib}

Name: openldap
Version: 2.4.24
Release: 6%{?dist}
Summary: LDAP support libraries
Group: System Environment/Daemons
License: OpenLDAP
URL: http://www.openldap.org/
Source0: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1: ldap.init
Source2: ldap.sysconfig
Source3: README.evolution
Source4: ldap.tmpfiles

# patches for 2.4
Patch0: openldap-slapd-conf.patch
Patch1: openldap-manpages.patch
Patch2: openldap-security-pie.patch
Patch3: openldap-sql-linking.patch
Patch4: openldap-reentrant-gethostby.patch
Patch5: openldap-export-ldif.patch
Patch6: openldap-smbk5pwd-overlay.patch
Patch7: openldap-ldaprc-currentdir.patch
Patch8: openldap-userconfig-setgid.patch
Patch9: openldap-nss-nofork.patch
Patch10: openldap-nss-null-pointer.patch
Patch11: openldap-slapadd-hang.patch
Patch12: openldap-nss-cacertdir-soft-error.patch
Patch13: openldap-ldapexop-double-free.patch
Patch14: openldap-segfault-ldif-indent.patch
Patch15: openldap-segfault-ldif-nl-end.patch
Patch16: openldap-nss-init-threadsafe.patch
Patch17: openldap-nss-free-peer-cert.patch
Patch18: openldap-nss-reqcert-hostname.patch
Patch19: openldap-nss-verifycert.patch
Patch20: openldap-nss-memleak-free-certs.patch
Patch21: openldap-constraint-overlay-config.patch
Patch22: openldap-dds-overlay-tolerance.patch
Patch23: openldap-man-slapo-unique.patch
Patch24: openldap-nss-wildcards.patch
Patch25: openldap-man-ldap-sync.patch
Patch26: openldap-sasl-gssapi-options.patch
Patch27: openldap-nss-can-ignore-expired-issuer.patch
Patch28: openldap-sql-datatypes.patch
Patch29: openldap-nss-handshake-threadsafe.patch
Patch30: openldap-syncrepl-unset-tls-options.patch
Patch31: openldap-ld_defconn-rebind.patch

# patches for the evolution library (see README.evolution)
Patch200: openldap-evolution-ntlm.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cyrus-sasl-devel >= 2.1, nss-devel, krb5-devel, tcp_wrappers-devel, unixODBC-devel
BuildRequires: glibc-devel, libtool, libtool-ltdl-devel, groff, perl
# smbk5pwd overlay:
BuildRequires: openssl-devel

Obsoletes: compat-openldap < 2.4
# used by migrationtools:
Provides: ldif2ldbm

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package devel
Summary: LDAP development libraries and header files
Group: Development/Libraries
Requires: openldap = %{version}-%{release}, cyrus-sasl-devel >= 2.1
Provides: openldap-evolution-devel = %{version}-%{release}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package servers
Summary: LDAP server
License: OpenLDAP
Requires: openldap = %{version}-%{release}, openssl
Requires(pre): shadow-utils, initscripts
Requires(post): chkconfig, /sbin/runuser, make, initscripts
Requires(preun): chkconfig, initscripts
BuildRequires: db4-devel >= 4.4, db4-devel < 4.9
Group: System Environment/Daemons

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd server and related files.

%package servers-sql
Summary: SQL support module for OpenLDAP server
Requires: openldap-servers = %{version}-%{release}
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
Summary: LDAP client utilities
Requires: openldap = %{version}-%{release}
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
%setup -q -c -a 0

# setup tree for openldap

pushd openldap-%{version}

%patch0 -p1 -b .config
%patch1 -p1 -b .manpages
%patch2 -p1 -b .security-pie
%patch3 -p1 -b .sql-linking
%patch4 -p1 -b .reentrant-gethostby
%patch5 -p1 -b .export-ldif
%patch6 -p1 -b .smbk5pwd-overlay
%patch7 -p1 -b .ldaprc-currentdir
%patch8 -p1 -b .userconfig-setgid
%patch9 -p1 -b .nss-nofork
%patch10 -p1 -b .nss-null-pointer
%patch11 -p1 -b .slapadd-hang
%patch12 -p1 -b .nss-cacertdir-soft-error
%patch13 -p1 -b .ldapexop-double-free
%patch14 -p1 -b .segfault-ldif-indent
%patch15 -p1 -b .segfault-ldif-nl-end
%patch16 -p1 -b .nss-init-threadsafe
%patch17 -p1 -b .nss-free-peer-cert
%patch18 -p1 -b .nss-reqcert-hostname
%patch19 -p1 -b .nss-verifycert
%patch20 -p1 -b .nss-memleak-free-certs
%patch21 -p1 -b .constraint-overlay-config
%patch22 -p1 -b .dds-overlay-tolerance
%patch23 -p1 -b .man-slapo-unique
%patch24 -p1 -b .nss-wildcards
%patch25 -p1 -b .man-ldap-sync
%patch26 -p1 -b .sasl-gssapi-options
%patch27 -p1 -b .nss-can-ignore-expired-issuer
%patch28 -p1 -b .sql-datatypes
%patch29 -p1 -b .nss-handshake-threadsafe
%patch30 -p1 -b .syncrepl-unset-tls-options
%patch31 -p1 -b .ld_defconn-rebind

cp %{_datadir}/libtool/config/config.{sub,guess} build/

for subdir in build-servers build-clients ; do
	mkdir $subdir
	ln -s ../configure $subdir
done

# build smbk5pwd with other overlays
ln -s ../../../contrib/slapd-modules/smbk5pwd/smbk5pwd.c servers/slapd/overlays
mv contrib/slapd-modules/smbk5pwd/README contrib/slapd-modules/smbk5pwd/README.smbk5pwd

popd

# setup tree for openldap with evolution-specific patches

if ! cp -al openldap-%{version} evo-openldap-%{version} ; then
	rm -fr evo-openldap-%{version}
	cp -a  openldap-%{version} evo-openldap-%{version}
fi
pushd evo-openldap-%{version}
%patch200 -p1 -b .evolution-ntlm
popd

%build

libtool='%{_bindir}/libtool'
export tagname=CC

%ifarch ia64
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -O0"
%endif

export CPPFLAGS="-I%_includedir/nss3 -I%_includedir/nspr4"
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS -fPIC -D_REENTRANT -DLDAP_CONNECTIONLESS -D_GNU_SOURCE -DHAVE_TLS -DHAVE_MOZNSS -DSLAPD_LMHASH"
export NSS_LIBS="-lssl3 -lsmime3 -lnss3 -lnssutil3 -lplds4 -lplc4 -lnspr4"
export LIBS=""

build() {

%configure \
    --with-threads=posix \
    \
    --enable-local \
	--enable-rlookups \
    \
    --with-tls=no \
    --with-cyrus-sasl \
    \
    --with-wrappers \
    \
    --enable-passwd \
    \
    --enable-cleartext \
    --enable-crypt \
    --enable-spasswd \
    --disable-lmpasswd \
    --enable-modules \
    --disable-sql \
    \
    --libexecdir=%{_libdir} \
    $@

# allow #include <nss/file.h> and <nspr/file.h>
pushd include
if [ ! -d nss ] ; then
    ln -s %{_includedir}/nss3 nss
fi
if [ ! -d nspr ] ; then
    ln -s %{_includedir}/nspr4 nspr
fi
popd

make %{_smp_mflags} LIBTOOL="$libtool"

}

# Kerberos support:
# - enabled in server (mainly for password checking)
# - disabled in clients (not needed, to avoid stray dependencies)

# build servers
export LIBS="$NSS_LIBS -lpthread"
pushd openldap-%{version}/build-servers
build \
    --enable-plugins \
    --enable-slapd \
    --enable-multimaster \
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
    --disable-ndb \
    --enable-passwd \
    --enable-sock \
    --disable-perl \
    --enable-relay \
    --disable-shared \
    --disable-dynamic \
    --with-kerberos=k5only \
    --enable-overlays=mod
popd

# build clients
export LIBS="$NSS_LIBS"
pushd openldap-%{version}/build-clients
build \
    --disable-slapd \
    --enable-shared \
    --enable-dynamic \
    --without-kerberos \
    --with-pic
popd

# build evolution-specific clients
# (specific patch, different installation directory, no shared libraries)
pushd evo-openldap-%{version}
build \
    --disable-slapd \
    --disable-shared \
    --disable-dynamic \
    --enable-static \
    --without-kerberos \
    --with-pic \
    --includedir=%{evolution_connector_includedir} \
    --libdir=%{evolution_connector_libdir}
popd

%install
rm -rf %{buildroot}
libtool='%{_bindir}/libtool'
export tagname=CC

mkdir -p %{buildroot}/%{_libdir}/

# install servers
pushd openldap-%{version}/build-servers
make install DESTDIR=%{buildroot} \
	libdir=%{_libdir} \
	LIBTOOL="$libtool" \
	STRIP=""
popd

# install evolution-specific clients (conflicting files will be overwriten by generic version)
pushd evo-openldap-%{version}
make install DESTDIR=%{buildroot} \
    includedir=%{evolution_connector_includedir} \
    libdir=%{evolution_connector_libdir} \
    LIBTOOL="$libtool" \
    STRIP=""
install -m 644 %SOURCE3 \
    %{buildroot}/%{evolution_connector_prefix}/
popd

# install clients
pushd openldap-%{version}/build-clients
make install DESTDIR=%{buildroot} \
	libdir=%{_libdir} \
	LIBTOOL="$libtool" \
	STRIP=""
popd

# setup directories for TLS certificates
mkdir -p %{buildroot}%{_sysconfdir}/openldap/cacerts
mkdir -p %{buildroot}%{_sysconfdir}/pki/tls/certs

# setup data and runtime directories
mkdir -p %{buildroot}/var/lib/ldap
mkdir -p %{buildroot}/var/run/openldap

# setup autocreation of runtime directories on tmpfs
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
install -m 644 %SOURCE4 %{buildroot}%{_sysconfdir}/tmpfiles.d/openldap.conf

# remove build root from config files and manual pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}/%{_sysconfdir}/openldap/*.conf
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

# we don't need the default files -- RPM handles changes
rm -f %{buildroot}/%{_sysconfdir}/openldap/*.default
rm -f %{buildroot}/%{_sysconfdir}/openldap/schema/*.default

# install an init script for the servers
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 %SOURCE1 %{buildroot}%{_sysconfdir}/rc.d/init.d/slapd

# install syconfig/ldap
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %SOURCE2 %{buildroot}%{_sysconfdir}/sysconfig/ldap

# move slapd out of _libdir
mv %{buildroot}/%{_libdir}/slapd %{buildroot}/%{_sbindir}/

# setup tools as symlinks to slapd
rm -f %{buildroot}/%{_sbindir}/slap{acl,add,auth,cat,dn,index,passwd,test,schema}
rm -f %{buildroot}/%{_libdir}/slap{acl,add,auth,cat,dn,index,passwd,test,schema}
for X in acl add auth cat dn index passwd test schema; do ln -s slapd %{buildroot}/%{_sbindir}/slap$X ; done

# tweak permissions on the libraries to make sure they're correct
chmod 755 %{buildroot}/%{_libdir}/lib*.so*
chmod 644 %{buildroot}/%{_libdir}/lib*.*a

# slapd.conf(5) is obsoleted since 2.3, see slapd-config(5)
# new configuration will be generated in %post
mkdir -p %{buildroot}/%{_datadir}/openldap-servers
mkdir %{buildroot}/%{_sysconfdir}/openldap/slapd.d
mv %{buildroot}/%{_sysconfdir}/openldap/slapd.conf %{buildroot}/%{_datadir}/openldap-servers/slapd.conf.obsolete
chmod 0644 %{buildroot}/%{_datadir}/openldap-servers/slapd.conf.obsolete

# move doc files out of _sysconfdir
mv %{buildroot}%{_sysconfdir}/openldap/schema/README README.schema
mv %{buildroot}%{_sysconfdir}/openldap/DB_CONFIG.example %{buildroot}/%{_datadir}/openldap-servers/DB_CONFIG.example
chmod 0644 openldap-%{version}/servers/slapd/back-sql/rdbms_depend/timesten/*.sh
chmod 0644 %{buildroot}/%{_datadir}/openldap-servers/DB_CONFIG.example

# remove files which we don't want packaged
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/*.a
rm -f %{buildroot}/%{evolution_connector_libdir}/*.la
rm -f %{buildroot}/%{evolution_connector_libdir}/*.so*
rm -f %{buildroot}/%{_libdir}/openldap/*.a
rm -f %{buildroot}/%{_libdir}/openldap/*.so

rm -f %{buildroot}%{_localstatedir}/openldap-data/DB_CONFIG.example
rmdir %{buildroot}%{_localstatedir}/openldap-data

%clean 
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%pre servers

# create ldap user and group
getent group ldap >/dev/null || groupadd -r -g 55 ldap
if ! getent passwd ldap >/dev/null; then
	useradd -r -g ldap -u 55 -d %{_sharedstatedir}/ldap -s /sbin/nologin -c "LDAP User" ldap
	# setup ownership of database files
	if [ -d /var/lib/ldap ] ; then
		for dbfile in /var/lib/ldap/* ; do
			if [ -f $dbfile ] ; then
				chown ldap:ldap $dbfile
			fi
		done
	fi
fi

# upgrade
if [ $1 -eq 2 ]; then
	# safe way to migrate the database if version number changed
	# http://www.openldap.org/doc/admin24/maintenance.html

	old_version=$(rpm -q --qf=%%{version} openldap-servers)
	new_version=%{version}

	if [ "$old_version" != "$new_version" ]; then
		pushd %{_sharedstatedir}/ldap &>/dev/null

		# stop the service
		if /sbin/service slapd status &>/dev/null; then
			touch need_start
			/sbin/service slapd stop
		else
			rm -f need_start
		fi

		if ls *.bdb &>/dev/null; then
			# symlink to last backup
			rm -f upgrade.ldif

			# backup location
			backupdir=backup.$(date +%%s)
			backupfile=${backupdir}/backup.ldif
			backupcmd="cp -a"

			mkdir -p ${backupdir}

			# database recovery tool
			# (this is necessary to handle upgrade from old openldap, which had embedded db4)
			if [ -f /usr/sbin/slapd_db_recover ]; then
				db_recover=/usr/sbin/slapd_db_recover
			else
				db_recover=/usr/bin/db_recover
			fi

			# make sure the database is consistent
			runuser -m -s $db_recover -- "ldap" -h %{_sharedstatedir}/ldap &>/dev/null

			# export the database if possible
			if [ $? -eq 0 ]; then
				if [ -f %{_sysconfdir}/openldap/slapd.conf ]; then
					slapcat -f %{_sysconfdir}/openldap/slapd.conf -l $backupfile &>/dev/null
				else
					slapcat -F %{_sysconfdir}/openldap/slapd.d -l $backupfile &>/dev/null
				fi

				if [ $? -eq 0 ]; then
					chmod 0400 $backupfile
					ln -sf $backupfile upgrade.ldif
					backupcmd=mv
				fi
			fi

			# move or copy to backup directory
			find -maxdepth 1 -type f \( -name alock -o -name "*.bdb" -o -name "__db.*" -o -name "log.*" \) \
				| xargs -I '{}' $backupcmd '{}' $backupdir
			cp -af DB_CONFIG $backupdir &>/dev/null

			# fix permissions
			chown -R ldap: $backupdir
			chmod -R a-w $backupdir
		fi

		popd &>/dev/null
	fi
fi

exit 0

%post servers

/sbin/ldconfig
/sbin/chkconfig --add slapd

# generate sample TLS certificates
if [ ! -f %{_sysconfdir}/pki/tls/certs/slapd.pem ] ; then
pushd %{_sysconfdir}/pki/tls/certs > /dev/null 2>&1
umask 077
cat << EOF | make slapd.pem > /dev/null 2>&1
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

# generate configuration in slapd.d
if ! ls -d %{_sysconfdir}/openldap/slapd.d/* &>/dev/null; then

	# fresh installation
	[ ! -f %{_sysconfdir}/openldap/slapd.conf ]
	fresh_install=$?

	[ $fresh_install -eq 0 ] && \
		cp %{_datadir}/openldap-servers/slapd.conf.obsolete %{_sysconfdir}/openldap/slapd.conf

	# convert from old style config slapd.conf
	mv %{_sysconfdir}/openldap/slapd.conf %{_sysconfdir}/openldap/slapd.conf.bak
	mkdir -p %{_sysconfdir}/openldap/slapd.d/
	lines=$(egrep -n '^(database|backend)' %{_sysconfdir}/openldap/slapd.conf.bak | cut -d: -f1 | head -n 1)
	lines=$(($lines-1))
	head -n $lines %{_sysconfdir}/openldap/slapd.conf.bak > %{_sysconfdir}/openldap/slapd.conf
	cat >> %{_sysconfdir}/openldap/slapd.conf << EOF
database config
rootdn   "cn=admin,cn=config"
#rootpw   secret
EOF
	lines_r=$(wc --lines %{_sysconfdir}/openldap/slapd.conf.bak | cut -f1 -d" ")
	lines_r=$(($lines_r-$lines))
	tail -n $lines_r %{_sysconfdir}/openldap/slapd.conf.bak >> %{_sysconfdir}/openldap/slapd.conf
	slaptest -f %{_sysconfdir}/openldap/slapd.conf -F %{_sysconfdir}/openldap/slapd.d > /dev/null 2> /dev/null
	chown -R ldap:ldap %{_sysconfdir}/openldap/slapd.d
	chmod -R 000 %{_sysconfdir}/openldap/slapd.d
	chmod -R u+rwX %{_sysconfdir}/openldap/slapd.d
	rm -f %{_sysconfdir}/openldap/slapd.conf
	rm -f %{_sharedstatedir}/ldap/__db* %{_sharedstatedir}/ldap/alock

	[ $fresh_install -eq 0 ] && rm -f %{_sysconfdir}/openldap/slapd.conf.bak
fi

# finish database migration (see %pre)
if [ -f %{_sharedstatedir}/ldap/upgrade.ldif ]; then
	runuser -m -s /usr/sbin/slapadd -- ldap -q -l %{_sharedstatedir}/ldap/upgrade.ldif &>/dev/null
	rm -f %{_sharedstatedir}/ldap/upgrade.ldif
fi

# restart after upgrade
if [ $1 -ge 1 ]; then
	if [ -f %{_sharedstatedir}/ldap/need_start ]; then
		/sbin/service slapd start
		rm -f %{_sharedstatedir}/ldap/need_start
	else
		/sbin/service slapd condrestart
	fi
fi

exit 0

%preun servers
if [ $1 -eq 0 ] ; then
	/sbin/service slapd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del slapd

	# openldap-servers are being removed from system
	# do not touch the database!
fi

%postun servers
/sbin/ldconfig

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%triggerin servers -- db4

# db4 upgrade (see %triggerun)
if [ $2 -eq 2 ]; then
	pushd %{_sharedstatedir}/ldap &>/dev/null

	# we are interested in minor version changes (both versions of db4 are installed at this moment)
	if [ "$(rpm -q --qf="%%{version}\n" db4 | sed 's/\.[0-9]*$//' | sort -u | wc -l)" != "1" ]; then
		# stop the service
		if /sbin/service slapd status &>/dev/null; then
			touch need_start
			/sbin/service slapd stop
		fi

		# ensure the database is consistent
		runuser -m -s /usr/bin/db_recover -- "ldap" -h %{_sharedstatedir}/ldap &>/dev/null

		# upgrade will be performed after removing old db4
		touch upgrade_db4
	else
		rm -f upgrade_db4
	fi

	popd &>/dev/null
fi

exit 0

%triggerun servers -- db4

# db4 upgrade (see %triggerin)
if [ -f %{_sharedstatedir}/ldap/upgrade_db4 ]; then
	pushd %{_sharedstatedir}/ldap &>/dev/null

	# perform the upgrade
	if ls *.bdb &>/dev/null; then
		runuser -m -s /usr/bin/db_upgrade -- "ldap" -h %{_sharedstatedir}/ldap %{_sharedstatedir}/ldap/*.bdb
		runuser -m -s /usr/bin/db_checkpoint -- "ldap" -h %{_sharedstatedir}/ldap -1
	fi

	# start the service
	if [ -f need_start ]; then
		/sbin/service slapd start
		rm -f need_start
	fi

	rm -f upgrade_db4
	popd &>/dev/null
fi

exit 0

%files
%defattr(-,root,root)
%doc openldap-%{version}/ANNOUNCEMENT
%doc openldap-%{version}/CHANGES
%doc openldap-%{version}/COPYRIGHT
%doc openldap-%{version}/LICENSE
%doc openldap-%{version}/README
%attr(0755,root,root) %dir %{_sysconfdir}/openldap
%attr(0755,root,root) %dir %{_sysconfdir}/openldap/cacerts
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/ldap*.conf
%attr(0755,root,root) %{_libdir}/libldif-2.4*.so.*
%attr(0755,root,root) %{_libdir}/liblber-2.4*.so.*
%attr(0755,root,root) %{_libdir}/libldap-2.4*.so.*
%attr(0755,root,root) %{_libdir}/libldap_r-2.4*.so.*
%attr(0644,root,root) %{_mandir}/man5/ldif.5*
%attr(0644,root,root) %{_mandir}/man5/ldap.conf.5*

%files servers
%defattr(-,root,root)
%doc openldap-%{version}/contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%doc openldap-%{version}/doc/guide/admin/*.html
%doc openldap-%{version}/doc/guide/admin/*.png
%doc README.schema
%attr(0640,root,ldap) %ghost %config(noreplace) %{_sysconfdir}/pki/tls/certs/slapd.pem
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/slapd
%attr(0750,ldap,ldap) %dir %config(noreplace) %{_sysconfdir}/openldap/slapd.d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ldap
%attr(0755,root,root) %dir %config(noreplace) %{_sysconfdir}/openldap/schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/*.schema*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/*.ldif
%attr(0755,root,root) %{_sbindir}/sl*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0644,root,root) %{_mandir}/man5/slapd*.5*
%attr(0644,root,root) %{_mandir}/man5/slapo-*.5*
%attr(0700,ldap,ldap) %dir /var/lib/ldap
%attr(0755,ldap,ldap) %dir /var/run/openldap
%{_sysconfdir}/tmpfiles.d
%attr(0755,root,root) %dir %{_libdir}/openldap
%attr(0755,root,root) %{_libdir}/openldap/[^b]*
%attr(0755,root,root) %dir %{_datadir}/openldap-servers
%attr(0644,root,root) %{_datadir}/openldap-servers/*
# obsolete configuration
%attr(0640,ldap,ldap) %ghost %config(noreplace,missingok) %{_sysconfdir}/openldap/slapd.conf
%attr(0640,ldap,ldap) %ghost %config(noreplace,missingok) %{_sysconfdir}/openldap/slapd.conf.bak

%files servers-sql
%defattr(-,root,root)
%doc openldap-%{version}/servers/slapd/back-sql/docs/*
%doc openldap-%{version}/servers/slapd/back-sql/rdbms_depend
%attr(0755,root,root) %{_libdir}/openldap/back_sql*.so.*
%attr(0755,root,root) %{_libdir}/openldap/back_sql.la

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%doc openldap-%{version}/doc/drafts openldap-%{version}/doc/rfc
%attr(0755,root,root) %{_libdir}/libl*.so
%attr(0644,root,root) %{_includedir}/*
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0755,root,root) %dir %{evolution_connector_prefix}
%attr(0644,root,root)      %{evolution_connector_prefix}/README*
%attr(0755,root,root) %dir %{evolution_connector_includedir}
%attr(0644,root,root)      %{evolution_connector_includedir}/*.h
%attr(0755,root,root) %dir %{evolution_connector_libdir}
%attr(0644,root,root)      %{evolution_connector_libdir}/*.a

%changelog
* Mon Mar 26 2012 Jan Synáček <jsynacek@redhat.com> 2.4.26-7
- fix: Re-binding to a failed connection can segfault (#784989)

* Mon Sep 12 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-5
- fix: SSL_ForceHandshake function is not thread safe (#701678)
- fix: allow unsetting of tls_* syncrepl options (#734187)

* Wed Aug 24 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-4
- fix: NSS_Init* functions are not thread safe (#731112)
- fix: memleak in tlsm_auth_cert_handler (#717730)
- fix: incorrect behavior of allow/try options of VerifyCert and TLS_REQCERT (#725819)
- fix: memleak - free the return of tlsm_find_and_verify_cert_key (#725818)
- fix: conversion of constraint overlay settings to cn=config is incorrect (#733067)
- fix: DDS overlay tolerance parametr doesn't function and breakes default TTL (#733069)
- manpage fix: errors in manual page slapo-unique (#733070)
- fix: matching wildcard hostnames in certificate Subject field does not work (#733073)
- manpage fix: wrong ldap_sync_destroy() prototype in ldap_sync(3) manpage (#717722)
- fix: cannot set SASL or GSSAPI options (#733056)
- fix: TLS_REQCERT=never ignored when the issuer certificate is expired (#722961)
- fix: OpenLDAP server segfaults when using back-sql (#733077)

* Tue Jun 28 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-3
- fix: openldap-servers scriptlets require initscripts package (#716857)
- fix: connection failure if TLS_CACERTDIR doesn't exist but TLS_REQCERT is set to 'never' (#716854)
- fix: segmentation fault caused by double-free in ldapexop (#699683)
- fix: segfault when input line in LDIF file is indented incorrectly (#716855)
- fix: segfault when LDIF input is not terminated by newline (#716858)

* Fri Mar 18 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-2
- new: system resource limiting for slapd using ulimit
- fix update: openldap can't use TLS after a fork() (#636956)
- fix: possible null pointer dereference in NSS implementation
- fix: openldap-servers upgrade hangs or do not upgrade the database (#664433)

* Mon Feb 14 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-1
- rebase to 2.4.24

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-8
- fix update: openldap can't use TLS after a fork() (#636956)

* Tue Jan 25 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-7
- fix: openldap can't use TLS after a fork() (#636956)
- fix: openldap-server upgrade gets stuck when the database is damaged (#664433)

* Thu Jan 20 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-6
- fix: some server certificates refused with inadequate type error (#668899)
- fix: default encryption strength dropped in switch to using NSS (#669446)
- systemd compatibility: add configuration file (#656647, #668223)

* Thu Jan 06 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-5
- initscript: slaptest with '-u' to skip database opening (#667768)
- removed slurpd options from sysconfig/ldap
- fix: verification of self issued certificates (#657984)

* Mon Nov 22 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-4
- Mozilla NSS - implement full non-blocking semantics
  ldapsearch -Z hangs server if starttls fails (#652822)
- updated list of all overlays in slapd.conf (#655899)
- fix database upgrade process (#656257)

* Thu Nov 18 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-3
- add support for multiple prefixed Mozilla NSS database files in TLS_CACERTDIR
- reject non-file keyfiles in TLS_CACERTDIR (#652315)
- TLS_CACERTDIR precedence over TLS_CACERT (#652304)
- accept only files in hash.0 format in TLS_CACERTDIR (#650288)
- improve SSL/TLS trace messages (#652818)

* Mon Nov 01 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-2
- fix possible infinite loop when checking permissions of TLS files (#641946)
- removed outdated autofs.schema (#643045)
- removed outdated README.upgrade
- removed relics of migrationtools

* Fri Aug 27 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-1
- rebase to 2.4.23
- embeded db4 library removed
- removed bogus links in "SEE ALSO" in several man-pages (#624616)

* Thu Jul 22 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.22-7
- Mozilla NSS - delay token auth until needed (#616552)
- Mozilla NSS - support use of self signed CA certs as server certs (#614545)

* Tue Jul 20 2010 Jan Vcelak <jvcelak@redhat.com> - 2.4.22-6
- CVE-2010-0211 openldap: modrdn processing uninitialized pointer free (#605448)
- CVE-2010-0212 openldap: modrdn processing IA5StringNormalize NULL pointer dereference (#605452)
- obsolete configuration file moved to /usr/share/openldap-servers (#612602)

* Thu Jul 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-5
- another shot at previous fix

* Thu Jul 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-4
- fixed issue with owner of /usr/lib/ldap/__db.* (#609523)

* Thu Jun  3 2010 Rich Megginson <rmeggins@redhat.com> - 2.4.22-3
- added ldif.h to the public api in the devel package
- added -lldif to the public api
- added HAVE_MOZNSS and other flags to use Mozilla NSS for crypto

* Tue May 18 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-2
- rebuild with connectionless support (#587722)
- updated autofs schema (#584808)

* Tue May 04 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-1
- rebased to 2.4.22 (mostly bugfixes, added back-ldif, back-null testing support)
- due to some possible issues pointed out in last update testing phase, I'm
  pulling back the last change (slapd can't be moved since it depends on /usr
  possibly mounted from network)

* Fri Mar 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-6
- moved slapd to start earlier during boot sequence

* Tue Mar 16 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-5
- minor corrections of init script (#571235, #570057, #573804)

* Wed Feb 24 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-4
- fixed SIGSEGV when deleting data using hdb (#562227)

* Mon Feb 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-3
- fixed broken link /usr/sbin/slapschema (#559873)

* Tue Jan 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-2
- removed some static libraries from openldap-devel (#556090)

* Mon Jan 11 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-1
- rebased openldap to 2.4.21
- rebased bdb to 4.8.26

* Mon Nov 23 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-3
- minor corrections in init script

* Mon Nov 16 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-2
- fixed tls connection accepting when TLSVerifyClient = allow
- /etc/openldap/ldap.conf removed from files owned by openldap-servers
- minor changes in spec file to supress warnings
- some changes in init script, so it would be possible to use it when
  using old configuration style

* Fri Nov 06 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-1
- rebased openldap to 2.4.19
- rebased bdb to 4.8.24

* Wed Oct 07 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-4
- updated smbk5pwd patch to be linked with libldap (#526500)
- the last buffer overflow patch replaced with the one from upstream
- added /etc/openldap/slapd.d and /etc/openldap/slapd.conf.bak
  to files owned by openldap-servers

* Thu Sep 24 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-3
- cleanup of previous patch fixing buffer overflow

* Tue Sep 22 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-2
- changed configuration approach. Instead od slapd.conf slapd
  is using slapd.d directory now
- fix of some issues caused by renaming of init script
- fix of buffer overflow issue in ldif.c pointed out by new glibc

* Fri Sep 18 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-1
- rebase of openldap to 2.4.18

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-7
- updated documentation (hashing the cacert dir)

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-6
- updated init script to be LSB-compliant (#523434)
- init script renamed to slapd

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.4.16-5
- rebuilt with new openssl

* Tue Aug 25 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-4
- updated %pre script to correctly install openldap group

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-1
- rebase of openldap to 2.4.16
- fixed minor issue in spec file (output looking interactive
  when installing servers)

* Tue Jun 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-4
- added $SLAPD_URLS variable to init script (#504504)

* Thu Apr 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-3
- extended previous patch (#481310) to remove options cfMP
  from some client tools
- correction of patch setugid (#494330)

* Thu Mar 26 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-2
- removed -f option from some client tools (#481310)

* Wed Feb 25 2009 Jan Safranek <jsafranek@redhat.com> 2.4.15-1
- new upstream release

* Tue Feb 17 2009 Jan Safranek <jsafranek@redhat.com> 2.4.14-1
- new upstream release
- upgraded to db-4.7.25

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 2.4.12-3
- rebuild with new openssl

* Mon Dec 15 2008 Caolán McNamara <caolanm@redhat.com> 2.4.12-2
- rebuild for libltdl, i.e. copy config.sub|guess from new location

* Wed Oct 15 2008 Jan Safranek <jsafranek@redhat.com> 2.4.12-1
- new upstream release

* Mon Oct 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-3
- add SLAPD_SHUTDOWN_TIMEOUT to /etc/sysconfig/ldap, allowing admins
  to set non-default slapd shutdown timeout
- add checkpoint to default slapd.conf file (#458679)

* Mon Sep  1 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-2
- provide ldif2ldbm functionality for migrationtools
- rediff all patches to get rid of patch fuzz

* Mon Jul 21 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-1
- new upstream release
- apply official bdb-4.6.21 patches

* Wed Jul  2 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-2
- fix CVE-2008-2952 (#453728)

* Thu Jun 12 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-1
- new upstream release

* Wed May 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-5
- use /sbin/nologin as shell of ldap user (#447919)

* Tue May 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-4
- new upstream release
- removed unnecessary MigrationTools patches

* Thu Apr 10 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-4
- bdb upgraded to 4.6.21
- reworked upgrade logic again to run db_upgrade when bdb version
  changes

* Wed Mar  5 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-3
- reworked the upgrade logic, slapcat/slapadd of the whole database
  is needed only if minor version changes (2.3.x -> 2.4.y)
- do not try to save database in LDIF format, if openldap-servers package 
  is  being removed (it's up to the admin to do so manually)

* Thu Feb 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-2
- migration tools carved out to standalone package "migrationtools"
  (#236697)

* Fri Feb 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-1
- new upstream release

* Fri Feb  8 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-7
- fix CVE-2008-0658 (#432014)

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-6
- init script fixes

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-5
- init script made LSB-compliant (#247012)

* Fri Jan 25 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-4
- fixed rpmlint warnings and errors
  - /etc/openldap/schema/README moved to /usr/share/doc/openldap

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-3
- obsoleting compat-openldap properly again :)

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-2
- obsoleting compat-openldap properly (#429591)

* Mon Jan 14 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-1
- new upstream version (openldap-2.4.7)

* Mon Dec  3 2007 Jan Safranek <jsafranek@redhat.com> 2.4.6-1
- new upstream version (openldap-2.4)
- deprecating compat- package

* Mon Nov  5 2007 Jan Safranek <jsafranek@redhat.com> 2.3.39-1
- new upstream release

* Tue Oct 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-4
- fixed multilib issues - all platform independent files have the
  same content now (#342791)

* Thu Oct  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-3
- BDB downgraded back to 4.4.20 because 4.6.18 is not supported by 
  openldap (#314821)

* Mon Sep 17 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-2
- skeleton /etc/sysconfig/ldap added
- new SLAPD_LDAP option to turn off listening on ldap:/// (#292591)
- fixed checking of SSL (#292611)
- fixed upgrade with empty database

* Thu Sep  6 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-1
- new upstream version
- added images to the guide.html (#273581)

* Wed Aug 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-3
- just rebuild

* Thu Aug  2 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-2
- do not use specific automake and autoconf
- do not distinguish between NPTL and non-NPTL platforms, we have NPTL
  everywhere
- db-4.6.18 integrated
- updated openldap-servers License: field to reference BDB license

* Tue Jul 31 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-1
- new upstream version

* Fri Jul 20 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-7
- MigrationTools-47 integrated

* Wed Jul  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-6
- fix compat-slapcat compilation. Now it can be found in 
  /usr/lib/compat-openldap/slapcat, because the tool checks argv[0]
  (#246581)

* Fri Jun 29 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-5
- smbk5pwd added (#220895)
- correctly distribute modules between servers and servers-sql packages

* Mon Jun 25 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-4
- Fix initscript return codes (#242667)
- Provide overlays (as modules; #246036, #245896)
- Add available modules to config file

* Tue May 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-3
- do not create script in /tmp on startup (bz#188298)
- add compat-slapcat to openldap-compat (bz#179378)
- do not import ddp services with migrate_services.pl
  (bz#201183)
- sort the hosts by adders, preventing duplicities
  in migrate*nis*.pl (bz#201540)
- start slupd for each replicated database (bz#210155)
- add ldconfig to devel post/postun (bz#240253)
- include misc.schema in default slapd.conf (bz#147805)

* Mon Apr 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-2
- slapadd during package update is now quiet (bz#224581)
- use _localstatedir instead of var/ during build (bz#220970)
- bind-libbind-devel removed from BuildRequires (bz#216851)
- slaptest is now quiet during service ldap start, if
  there is no error/warning (bz#143697)
- libldap_r.so now links with pthread (bz#198226)
- do not strip binaries to produce correct .debuginfo packages
  (bz#152516)

* Mon Feb 19 2007 Jay Fenlason <fenlason<redhat.com> 2.3.34-1
- New upstream release
- Upgrade the scripts for migrating the database so that they might
  actually work.
- change bind-libbind-devel to bind-devel in BuildPreReq

* Mon Dec  4 2006 Thomas Woerner <twoerner@redhat.com> 2.3.30-1.1
- tcp_wrappers has a new devel and libs sub package, therefore changing build
  requirement for tcp_wrappers to tcp_wrappers-devel

* Wed Nov 15 2006 Jay Fenlason <fenlason@redhat.com> 2.3.30-1
- New upstream version

* Wed Oct 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.28-1
- New upstream version

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.3.27-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-3
- Include --enable-multimaster to close
  bz#185821: adding slapd_multimaster to the configure options
- Upgade guide.html to the correct one for openladp-2.3.27, closing
  bz#190383: openldap 2.3 packages contain the administrator's guide for 2.2
- Remove the quotes from around the slaptestflags in ldap.init
  This closes one part of
  bz#204593: service ldap fails after having added entries to ldap
- include __db.* in the list of files to check ownership of in
  ldap.init, as suggested in
  bz#199322: RFE: perform cleanup in ldap.init

* Fri Aug 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-2
- New upstream release
- Include the gethostbyname_r patch so that nss_ldap won't hang
  on recursive attemts to ldap_initialize.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.24-2.1
- rebuild

* Wed Jun 7 2006 Jay Fenlason <fenlason@redhat.com> 2.3.24-2
- New upstream version

* Thu Apr 27 2006 Jay Fenlason <fenlason@redhat.com> 2.3.21-2
- Upgrade to 2.3.21
- Add two upstream patches for db-4.4.20

* Mon Feb 13 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-4
- Re-fix ldap.init

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-3.1
- bump again for double-long bug on ppc(64)

* Thu Feb 9 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-3
- Modify the ldap.init script to call runuser correctly.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-2
- Upgrade to 2.3.19, which upstream now considers stable
- Modify the -config.patch, ldap.init, and this spec file to put the
  pid file and args file in an ldap-owned openldap subdirectory under
  /var/run.
- Move back_sql* out of _sbindir/openldap , which requires
  hand-moving slapd and slurpd to _sbindir, and recreating symlinks
  by hand.
- Retire openldap-2.3.11-ads.patch, which went upstream.
- Update the ldap.init script to run slaptest as the ldap user rather
  than as root.  This solves
  bz#150172 Startup failure after database problem
- Add to the servers post and preun scriptlets so that on preun, the
  database is slapcatted to /var/lib/ldap/upgrade.ldif and the
  database files are saved to /var/lib/ldap/rpmorig.  On post, if
  /var/lib/ldap/upgrade.ldif exists, it is slapadded.  This means that
  on upgrades from 2.3.16-2 to higher versions, the database files may
  be automatically upgraded.  Unfortunatly, because of the changes to
  the preun scriptlet, users have to do the slapcat, etc by hand when
  upgrading to 2.3.16-2.  Also note that the /var/lib/ldap/rpmorig
  files need to be removed by hand because automatically removing your
  emergency fallback files is a bad idea.
- Upgrade internal bdb to db-4.4.20.  For a clean upgrade, this will
  require that users slapcat their databases into a temp file, move
  /var/lib/ldap someplace safe, upgrade the openldap rpms, then
  slapadd the temp file.


* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-3
- Remove Requires: cyrus-sasl and cyrus-sasl-md5 from openldap- and
  compat-openldap- to close
  bz#173313 Remove exlicit 'Requires: cyrus-sasl" + 'Requires: cyrus-sasl-md5'

* Thu Nov 10 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-2
- Upgrade to 2.3.11, which upstream now considers stable.
- Switch compat-openldap to 2.2.29
- remove references to nss_ldap_build from the spec file
- remove references to 2.0 and 2.1 from the spec file.
- reorganize the build() function slightly in the spec file to limit the
  number of redundant and conflicting options passedto configure.
- Remove the attempt to hardlink ldapmodify and ldapadd together, since
  the current make install make ldapadd a symlink to ldapmodify.
- Include the -ads patches to allow SASL binds to an Active Directory
  server to work.  Nalin <nalin@redhat.com> wrote the patch, based on my
  broken first attempt.

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 2.2.29-3
- rebuilt against new openssl

* Mon Oct 10 2005 Jay Fenlason <fenlason@redhat.com> 2.2.29-2
- New upstream version.

* Thu Sep 29 2005 Jay Fenlason <fenlason@redhat.com> 2.2.28-2
- Upgrade to nev upstream version.  This makes the 2.2.*-hop patch obsolete.

* Mon Aug 22 2005 Jay Fenlason <fenlason@redhat.com> 2.2.26-2
- Move the slapd.pem file to /etc/pki/tls/certs
  and edit the -config patch to match to close
  bz#143393  Creates certificates + keys at an insecure/bad place
- also use _sysconfdir instead of hard-coding /etc

* Thu Aug 11 2005 Jay Fenlason <fenlason@redhat.com> 
- Add the tls-fix-connection-test patch to close
  bz#161991 openldap password disclosure issue
- add the hop patches to prevent infinite looping when chasing referrals.
  OpenLDAP ITS #3578

* Fri Aug  5 2005 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in ldap.init (call $klist instead of klist, from Charles Lopes)

* Thu May 19 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.26-1
- run slaptest with the -u flag if no id2entry db files are found, because
  you can't check for read-write access to a non-existent database (#156787)
- add _sysconfdir/openldap/cacerts, which authconfig sets as the
  TLS_CACERTDIR path in /etc/openldap/ldap.conf now
- use a temporary wrapper script to launch slapd, in case we have arguments
  with embedded whitespace (#158111)

* Wed May  4 2005 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.26 (stable 20050429)
- enable the lmpasswd scheme
- print a warning if slaptest fails, slaptest -u succeeds, and one of the
  directories listed as the storage location for a given suffix in slapd.conf
  contains a readable file named __db.001 (#118678)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.25-1
- update to 2.2.25 (release)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.24-1
- update to 2.2.24 (stable 20050318)
- export KRB5_KTNAME in the init script, in case it was set in the sysconfig
  file but not exported

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-4
- prefer libresolv to libbind

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-3
- add bind-libbind-devel and libtool-ltdl-devel buildprereqs

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 2.2.23-2
- rebuild with openssl-0.9.7e

* Mon Jan 31 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-1
- update to 2.2.23 (stable-20050125)
- update notes on upgrading from earlier versions
- drop slapcat variations for 2.0/2.1, which choke on 2.2's config files

* Tue Jan  4 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.20-1
- update to 2.2.20 (stable-20050103)
- warn about unreadable krb5 keytab files containing "ldap" keys
- warn about unreadable TLS-related files
- own a ref to subdirectories which we create under _libdir/tls

* Tue Nov  2 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.17-0
- rebuild

* Thu Sep 30 2004 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.17 (stable-20040923) (#135188)
- move nptl libraries into arch-specific subdirectories on x86 boxes
- require a newer glibc which can provide nptl libpthread on i486/i586

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com>
- move slapd startup to earlier in the boot sequence (#103160)
- update to 2.2.15 (stable-20040822)
- change version number on compat-openldap to include the non-compat version
  from which it's compiled, otherwise would have to start 2.2.15 at release 3
  so that it upgrades correctly

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-2
- build a separate, static set of libraries for openldap-devel with the
  non-standard ntlm bind patch applied, for use by the evolution-connector
  package (#125579), and installing them under
  evolution_connector_prefix)
- provide openldap-evolution-devel = version-release in openldap-devel
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
- change LD_FLAGS to refer to /usr/kerberos/_libdir instead of
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
