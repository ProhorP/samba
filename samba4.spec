%set_verify_elf_method unresolved=relaxed
%add_findprov_skiplist /%_lib/*
%add_debuginfo_skiplist /%_lib

%define rname samba
%define _localstatedir /var

# internal libs
%def_without talloc
%def_without tevent
%def_without tdb
%def_without ntdb
%def_without ldb
%def_with    winbind

%def_with profiling_data

# build as separate package
%def_without libsmbclient
%def_without libwbclient
%def_without libnetapi
%def_with docs

%def_with dc
%def_without ntvfs
%def_with clustering_support
%def_without testsuite

%if_with testsuite
# The testsuite only works with a full build right now.
%force_with dc
%endif

%if_with dc
# Samba Active Directory Domain Controller implementation is not available with MIT Kereberos
%def_without mitkrb5
%else
%def_with mitkrb5
%endif

%def_with systemd
%def_enable avahi
%def_enable glusterfs
%def_with libcephfs

Name:    samba-DC
Version: 4.4.14
Release: alt0.M70C.1

Group:   System/Servers
Summary: Samba Active Directory Domain Controller
License: GPLv3+ and LGPLv3+
Url:     http://www.samba.org/

Source:  %rname-%version.tar

# Red Hat specific replacement-files
Source1: samba.log
Source5: smb.init
Source6: samba.pamd
Source8: winbind.init
Source9: smb.conf.default
Source10: nmb.init
Source11: pam_winbind.conf
Source12: ctdb.init
Source20: samba.init

Source200: README.dc
Source201: README.downgrade

Patch: %rname-%version-%release.patch
Patch10: samba-grouppwd.patch

# fedora patches
Patch100:         samba-4.4.2-s3-winbind-make-sure-domain-member-can-talk-to-trust.patch

Conflicts: %rname
Conflicts: %rname-dc

# Need for samba_upgradedns
Requires: tdb-utils
Requires(pre): %name-common = %version-%release
Requires: %name-libs = %version-%release
%if_with winbind
Requires: %name-winbind-clients = %version-%release
%endif
%if_with libwbclient
Requires: libwbclient-DC = %version-%release
%endif

BuildRequires: /proc
BuildRequires: libe2fs-devel
BuildRequires: libacl-devel
BuildRequires: libattr-devel
BuildRequires: libgnutls-devel
BuildRequires: libncurses-devel
BuildRequires: libpam-devel
BuildRequires: perl-devel
BuildRequires: perl-Parse-Yapp
BuildRequires: libpopt-devel
BuildRequires: python-devel
BuildRequires: libreadline-devel
BuildRequires: libldap-devel
BuildRequires: zlib-devel
BuildRequires: libarchive-devel >= 3.1.2

%if_with mitkrb5
BuildRequires: libssl-devel
BuildRequires: libkrb5-devel
%endif
BuildRequires: glibc-devel glibc-kernheaders
# https://bugzilla.samba.org/show_bug.cgi?id=9863
BuildConflicts: setproctitle-devel
BuildRequires: libiniparser-devel
BuildRequires: libcups-devel
BuildRequires: gawk libgtk+2-devel libcap-devel libuuid-devel
BuildRequires: inkscape libxslt xsltproc netpbm dblatex html2text docbook-style-xsl
%{?_without_talloc:BuildRequires: libtalloc-devel >= 2.1.4 libpytalloc-devel}
%{?_without_tevent:BuildRequires: libtevent-devel >= 0.9.18 python-module-tevent}
%{?_without_tdb:BuildRequires: libtdb-devel >= 1.2.11  python-module-tdb}
%{?_without_ntdb:BuildRequires: libntdb-devel >= 0.9  python-module-ntdb}
%{?_without_ldb:BuildRequires: libldb-devel >= 1.1.21 python-module-pyldb-devel}
%{?_with_testsuite:BuildRequires: ldb-tools}
%{?_with_systemd:BuildRequires: systemd-devel}
%{?_enable_avahi:BuildRequires: libavahi-devel}
%{?_enable_glusterfs:BuildRequires: glusterfs3-devel >= 3.4.0.16}
%{?_with_libcephfs:BuildRequires: ceph-devel}

%description
Samba is the standard Windows interoperability suite of programs for Linux and Unix.

%package client
Summary: Samba client programs
Group: Networking/Other
Requires: %name-common = %version-%release
Requires: %name-libs = %version-%release
%if_with libsmbclient
Requires: libsmbclient-DC = %version-%release
%endif
Conflicts: %rname-client

%description client
The %rname-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.

%package common
Summary: Files used by both Samba servers and clients
Group: System/Servers
Requires: %name-libs = %version-%release
%if_with libnetapi
Requires: libnetapi-DC = %version-%release
%endif
Conflicts: %rname-common

%description common
%rname-common provides files necessary for both the server and client
packages of Samba.

%package libs
Summary: Samba libraries
Group: System/Libraries
Conflicts: %rname-libs
Conflicts: %rname-dc-libs

%if_with libnetapi
Requires: libnetapi-DC = %version-%release
%endif
%if_with libwbclient
Requires: libwbclient-DC = %version-%release
%endif
%if_with libsmbclient
Requires: libsmbclient-DC = %version-%release
%endif

%description libs
The %rname-libs package contains the libraries needed by programs that
link against the SMB, RPC and other protocols provided by the Samba suite.

%package -n libsmbclient-DC
Summary: The SMB client library
Group: System/Libraries
Conflicts: libsmbclient

%description -n libsmbclient-DC
The libsmbclient contains the SMB client library from the Samba suite.

%package -n libsmbclient-DC-devel
Summary: Developer tools for the SMB client library
Group: Development/C
Requires: libsmbclient-DC = %version-%release
Conflicts: libsmbclient-devel

%description -n libsmbclient-DC-devel
The libsmbclient-devel package contains the header files and libraries needed to
develop programs that link against the SMB client library in the Samba suite.

%package -n libwbclient-DC
Summary: The winbind client library
Group: System/Libraries
Conflicts: libwbclient

%description -n libwbclient-DC
The libwbclient package contains the winbind client library from the Samba suite.

%package -n libwbclient-DC-devel
Summary: Developer tools for the winbind library
Group: Development/C
Requires: libwbclient-DC = %version-%release
Conflicts: libwbclient-devel

%description -n libwbclient-DC-devel
The libwbclient-devel package provides developer tools for the wbclient library.

%package -n libnetapi-DC
Summary: Samba netapi library
Group: System/Libraries
Conflicts: libnetapi

%description -n libnetapi-DC
Samba netapi library

%package -n libnetapi-DC-devel
Summary: Samba netapi development files
Group: Development/Other
Requires: libnetapi-DC = %version-%release
Conflicts: libnetapi-devel

%description -n libnetapi-DC-devel
Samba netapi development files

%package -n python-module-%name
Summary: Samba Python libraries
Group: Networking/Other
Requires: %name-libs = %version-%release

%add_python_req_skip Tdb

%description -n python-module-%name
The %rname-python package contains the Python libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python programs.

%package devel
Summary: Developer tools for Samba libraries
Group: Development/C
Requires: %name-libs = %version-%release
Conflicts: %rname-devel

%description devel
The %rname-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.

%package pidl
Summary: Perl IDL compiler
Group: Development/Tools
BuildArch: noarch
# Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Conflicts: %rname-pidl

%description pidl
The %rname-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols

%package test
Summary: Testing tools for Samba servers and clients
Group: Development/Tools
Requires: %name = %version-%release
Requires: %name-common = %version-%release
Requires: %name-libs = %version-%release
%if_with winbind
Requires: %name-winbind = %version-%release
%endif
%if_with libsmbclient
Requires: libsmbclient-DC = %version-%release
%endif
Conflicts: %rname-test

%description test
samba4-test provides testing tools for both the server and client
packages of Samba.

%if_with winbind
%package winbind
Summary: Samba winbind
Group: System/Servers
Requires: %name-common = %version-%release
Requires: %name-libs = %version-%release
Conflicts: %rname-winbind

%description winbind
The %rname-winbind package provides the winbind NSS library, and some
client tools.  Winbind enables Linux to be a full member in Windows
domains and to use Windows user and group accounts on Linux.

%package winbind-clients
Summary: Samba winbind clients
Group: System/Servers
Requires: %name-winbind = %version-%release
%if_with libwbclient
Requires: libwbclient-DC = %version-%release
%endif

%description winbind-clients
The samba-winbind-clients package provides the NSS library and a PAM
module necessary to communicate to the Winbind Daemon

%package winbind-krb5-locator
Summary: Samba winbind krb5 locator
Group: System/Servers
%if_with libwbclient
Requires: libwbclient-DC = %version-%release
Requires: %name-winbind = %version-%release
%else
Requires: %name-libs = %version-%release
%endif
Conflicts: %rname-winbind-krb5-locator

%description winbind-krb5-locator
The winbind krb5 locator is a plugin for the system kerberos library to allow
the local kerberos library to use the same KDC as samba and winbind use

%package winbind-devel
Summary: Developer tools for the winbind library
Group: Development/C
Requires: %name-winbind = %version-%release
Conflicts: %rname-winbind-devel

%description winbind-devel
The samba-winbind package provides developer tools for the wbclient library.
%endif

%if_with clustering_support
%package ctdb
Summary: A Clustered Database based on Samba's Trivial Database (TDB)
Group: System/Servers

Requires: %name-libs = %version-%release

# for ps and killall
Requires: psmisc
Requires: tdb-utils
# for pkill and pidof:
Requires: procps
# for netstat:
Requires: net-tools
Requires: ethtool
# for ip:
Requires: iproute
Requires: iptables
# for flock, getopt, kill:
Requires: util-linux
Conflicts: ctdb

%description ctdb
CTDB is a cluster implementation of the TDB database used by Samba and other
projects to store temporary data. If an application is already using TDB for
temporary data it is very easy to convert that application to be cluster aware
and use CTDB instead.

%package ctdb-tests
Summary: CTDB clustered database test suite
Group: Development/Other
Requires: %name-libs = %version-%release
Requires: %name-ctdb = %version-%release
Requires: nc
Conflicts: ctdb-tests
Conflicts: ctdb-devel
Provides:  %name-ctdb-devel = %version-%release
Obsoletes: %name-ctdb-devel < %version-%release

%description ctdb-tests
Test suite for CTDB.
CTDB is a cluster implementation of the TDB database used by Samba and other
projects to store temporary data. If an application is already using TDB for
temporary data it is very easy to convert that application to be cluster aware
and use CTDB instead.
%endif

%if_with docs
%package doc
Summary: Documentation for the Samba suite
Group: Documentation
Requires: %name-common = %version-%release
BuildArch: noarch
Conflicts: %rname-doc

%description doc
The samba-doc package includes all the non-manpage documentation for the
Samba suite.
%endif

%package -n task-samba-dc
Summary: Samba Active Directory Domain Controller
Group: System/Servers
BuildArch: noarch
Provides: task-samba-ad-dc = %version-%release
Provides: task-ad-dc = %version-%release
Requires: samba-DC python-module-samba-DC samba-DC-common samba-DC-winbind-clients samba-DC-winbind samba-DC-client samba-DC-doc krb5-kinit
Conflicts: samba python-module-samba samba-common samba-winbind-clients samba-winbind samba-client samba-doc

%description -n task-samba-dc
Samba server acts as a Domain Controller that is compatible with
Microsoft Active Directory.

%package util-private-headers
Summary: libsamba_util private headers
Group: Development/C

%description util-private-headers
libsamba_util private headers.

%prep
%setup -q -n %rname-%version
%patch -p1
%patch10 -p1
%patch100 -p 1 -b .samba-4.4.2-s3-winbind-make-sure-domain-member-can-talk-to-trust.patch

%build

%define _talloc_lib ,talloc,pytalloc,pytalloc-util
%if_without talloc
%define _talloc_lib ,!talloc,!pytalloc,!pytalloc-util
%endif

%define _tevent_lib ,tevent,pytevent
%if_without tevent
%define _tevent_lib ,!tevent,!pytevent
%endif

%define _tdb_lib ,tdb,pytdb
%if_without tdb
%define _tdb_lib ,!tdb,!pytdb
%endif

%define _ntdb_lib ,ntdb,pyntdb
%if_without ntdb
%define _ntdb_lib ,!ntdb,!pyntdb
%endif

%define _ldb_lib ,ldb,pyldb,pyldb-util
%if_without ldb
%define _ldb_lib ,!ldb,!pyldb,!pyldb-util
%endif

%define _samba4_libraries heimdal,!zlib,!popt%{_talloc_lib}%{_tevent_lib}%{_tdb_lib}%{_ntdb_lib}%{_ldb_lib}

%define _samba4_idmap_modules idmap_ad,idmap_rid,idmap_adex,idmap_hash,idmap_tdb2
%define _samba4_pdb_modules pdb_tdbsam,pdb_ldap,pdb_ads,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4
%define _samba4_auth_modules auth_unix,auth_wbc,auth_server,auth_netlogond,auth_script,auth_samba4
# auth_domain needs to be static
%define _samba4_modules %_samba4_idmap_modules,%_samba4_pdb_modules,%_samba4_auth_modules

%define _libsmbclient %nil
%if_without libsmbclient
%define _libsmbclient smbclient,smbsharemodes,
%endif

%define _libwbclient %nil
%if_without libwbclient
%define _libwbclient wbclient,
%endif

%define _libnetapi %nil
%if_without libnetapi
%define _libnetapi netapi,
%endif

%define _samba4_private_libraries %{_libsmbclient}%{_libwbclient}%{_libnetapi}

%undefine _configure_gettext
%if_with mitkrb5
%add_optflags -I/usr/include/krb5
%endif
#LDFLAGS="-Wl,-z,relro,-z,now" \
%if_with dc
%define _samba_libdir  %_libdir/samba-dc
%define _samba_mod_libdir  %_libdir/samba-dc
%else
%define _samba_libdir  %_libdir
%define _samba_mod_libdir  %_libdir/samba
%endif

%configure \
	--enable-fhs \
	--with-piddir=/var/run \
	--with-sockets-dir=/var/run/samba \
	--libdir=%_samba_libdir \
	--with-modulesdir=%_samba_mod_libdir \
	--with-privatelibdir=%_samba_mod_libdir \
	--with-pammodulesdir=%_lib/security \
	--with-lockdir=%_localstatedir/lib/samba \
	--with-cachedir=%_localstatedir/cache/samba \
	--with-privatedir=/var/lib/samba/private \
	--with-shared-modules=%_samba4_modules \
	--bundled-libraries=%_samba4_libraries \
	--with-pam \
	--with-ads \
	--with-pie \
	--with-relro \
	--without-fam \
	--private-libraries=%_samba4_private_libraries \
%if_with mitkrb5
	--with-system-mitkrb5 \
%endif
%if_without dc
	--without-ad-dc \
%endif
%if_with systemd
	--with-systemd \
%else
	--without-systemd \
%endif
%if_with winbind
	--with-winbind \
%else
	--without-winbind \
%endif
%if_with clustering_support
	--with-cluster-support \
%endif
%if_with testsuite
	--enable-selftest \
%endif
%if_with profiling_data
	--with-profiling-data \
%endif
%if_with ntvfs
       --with-ntvfs-fileserver \
%endif
	%{subst_enable avahi}

[ -n "$NPROCS" ] || NPROCS=%__nprocs; export JOBS=$NPROCS
%make_build NPROCS=%__nprocs

%if_with docs
pushd docs-xml
export XML_CATALOG_FILES="file:///etc/xml/catalog file://$(pwd)/build/catalog.xml"
%autoreconf
%configure
%make_build smbdotconf/parameters.all.xml
%make_build release
popd
%endif

%install
%make install DESTDIR=%buildroot

mkdir -p %buildroot/sbin
mkdir -p %buildroot/usr/{sbin,bin}
mkdir -p %buildroot/%_lib/security
mkdir -p %buildroot/var/lib/samba
mkdir -p %buildroot/var/lib/ctdb
mkdir -p %buildroot%_localstatedir/cache/samba
mkdir -p %buildroot/var/lib/samba/{private,winbindd_privileged,scripts,sysvol}
mkdir -p %buildroot/var/log/samba/old
mkdir -p %buildroot/var/spool/samba
mkdir -p %buildroot/var/run/{samba,winbindd}
mkdir -p %buildroot%_samba_mod_libdir
mkdir -p %buildroot%_pkgconfigdir
mkdir -p %buildroot%_initdir
mkdir -p %buildroot%_unitdir
mkdir -p %buildroot%_sysconfdir/{pam.d,logrotate.d,security,sysconfig}
mkdir -p %buildroot/lib/tmpfiles.d

# Install other stuff
install -m644 %SOURCE1 %buildroot%_sysconfdir/logrotate.d/samba
install -m644 %SOURCE9 %buildroot%_sysconfdir/samba/smb.conf
install -m644 %SOURCE11 %buildroot%_sysconfdir/security
install -m644 %SOURCE6 %buildroot%_sysconfdir/pam.d/samba
echo 127.0.0.1 localhost > %buildroot%_sysconfdir/samba/lmhosts
mkdir -p %buildroot%_sysconfdir/openldap/schema
install -m644 examples/LDAP/samba.schema %buildroot%_sysconfdir/openldap/schema/samba.schema
install -m755 packaging/printing/smbprint %buildroot%_bindir/smbprint


install -m644 packaging/systemd/samba.sysconfig %buildroot%_sysconfdir/sysconfig/samba
install -m644 packaging/RHEL/setup/smbusers %buildroot%_sysconfdir/samba/smbusers

install -m755 %SOURCE10 %buildroot%_initrddir/nmb
install -m755 %SOURCE5 %buildroot%_initrddir/smb
install -m755 %SOURCE8 %buildroot%_initrddir/winbind
%if_with dc
install -m755 %SOURCE20 %buildroot%_initrddir/samba
%endif

# Put README in builddir
cp %SOURCE200 %SOURCE201 .

for i in nmb smb winbind samba; do
    cat packaging/systemd/$i.service | sed -e 's@\[Service\]@[Service]\nEnvironment=KRB5CCNAME=FILE:/run/samba/krb5cc_samba@g' >tmp$i.service
    install -m 0644 tmp$i.service %buildroot%_unitdir/$i.service
done
subst 's,Type=notify,Type=forking,' %buildroot%_unitdir/*.service
%if_with clustering_support
install -m755 %SOURCE12 %buildroot%_initrddir/ctdb
install -m 0644 ctdb/config/ctdb.service %buildroot%_unitdir
install -m 0644 ctdb/config/ctdb.sysconfig %buildroot%_sysconfdir/sysconfig/ctdb
echo "d /var/run/ctdb 755 root root" >> %buildroot%_tmpfilesdir/ctdb.conf
touch %buildroot%_sysconfdir/ctdb/nodes
%endif

install -m644 packaging/systemd/samba.conf.tmp %buildroot%_tmpfilesdir/%rname.conf

# NetworkManager online/offline script
install -d -m 0755 %buildroot%_sysconfdir/NetworkManager/dispatcher.d/
install -m 0755 packaging/NetworkManager/30-winbind-systemd \
            %buildroot%_sysconfdir/NetworkManager/dispatcher.d/30-winbind


# Clean out crap left behind by the PIDL install.
find %buildroot -type f -name .packlist -exec rm -f {} \;
rm -f %buildroot%perl_vendorlib/wscript_build
rm -rf %buildroot%perl_vendorlib/Parse/Yapp

# winbind
%if_with winbind
mkdir -p %buildroot/%_lib
ln -sf ..%_samba_libdir/libnss_winbind.so %buildroot/%_lib/libnss_winbind.so.2
ln -sf ..%_samba_libdir/libnss_wins.so    %buildroot/%_lib/libnss_wins.so.2

mkdir -p  %buildroot%_libdir/krb5/plugins/libkrb5
mv %buildroot%_samba_libdir/winbind_krb5_locator.so %buildroot%_libdir/krb5/plugins/libkrb5/
%endif

#cups backend
%define cups_serverbin %(cups-config --serverbin 2>/dev/null)
mkdir -p %buildroot%{cups_serverbin}/backend
ln -s %_bindir/smbspool %buildroot%{cups_serverbin}/backend/smb

# Fix up permission on perl install.
%_fixperms %buildroot%perl_vendor_privlib

# remove tests form python modules
rm -rf %buildroot%python_sitelibdir/samba/{tests,external/subunit,external/testtool}

# move pkgconfig to standart path:
[ "%_libdir" != "%_samba_libdir" ] && mv %buildroot{%_samba_libdir/pkgconfig,%_libdir}

# Install documentation
%if_with docs
mkdir -p %buildroot%_defaultdocdir/%rname/
cp -a docs-xml/output/htmldocs %buildroot%_defaultdocdir/%rname/
%endif

# Cleanup man pages
%if_without libsmbclient
/bin/rm -f %buildroot%_man7dir/libsmbclient.7*
%endif

# Install pidl/lib/Parse/Pidl/Samba3/Template.pm
cp -a pidl/lib/Parse/Pidl/Samba3/Template.pm %buildroot%_datadir/perl5/Parse/Pidl/Samba3/

# Copy libsamba_util private headers
mkdir -p %buildroot%_includedir/samba-4.0/private/lib/util/charset
cp lib/util/*.h %buildroot%_includedir/samba-4.0/private/lib/util
cp lib/util/charset/*.h %buildroot%_includedir/samba-4.0/private/lib/util/charset
mkdir -p %buildroot%_includedir/samba-4.0/private/libcli/util
cp libcli/util/*.h %buildroot%_includedir/samba-4.0/private/libcli/util
subst 's,\.\./,,' %buildroot%_includedir/samba-4.0/private/lib/util/*.h

%find_lang pam_winbind
%find_lang net

%if_with testsuite
%check
TDB_NO_FSYNC=1 %make_build test
%endif

%post
%if_with dc
%post_service samba
%else
%post_service smb
%post_service nmb
%endif

%preun
%if_with dc
%preun_service samba
%else
%preun_service smb
%preun_service nmb
%endif

%if_with winbind
%pre winbind
%_sbindir/groupadd -f -r wbpriv >/dev/null 2>&1 || :

%post winbind
%post_service winbind

%preun winbind
%preun_service winbind
%endif

%files
%doc COPYING README WHATSNEW.txt
%doc examples/autofs examples/LDAP examples/misc
%doc examples/printer-accounting examples/printing
%doc README.downgrade
%_bindir/smbstatus
%_bindir/eventlogadm
%_sbindir/nmbd
%_sbindir/smbd
%config(noreplace) %_sysconfdir/samba/smbusers
%attr(755,root,root) %_initdir/smb
%attr(755,root,root) %_initdir/nmb
%_unitdir/nmb.service
%_unitdir/smb.service
%attr(1777,root,root) %dir /var/spool/samba
%_sysconfdir/openldap/schema/samba.schema
%_sysconfdir/pam.d/samba
%_man1dir/smbstatus.1*
%_man8dir/eventlogadm.8*
%_man8dir/smbd.8*
%_man8dir/nmbd.8*
%_man8dir/vfs_*.8*

%if_with dc
%attr(755,root,root) %_initdir/samba
%_unitdir/samba.service
%_bindir/samba-tool
%_sbindir/samba
%_sbindir/samba_kcc
%_sbindir/samba_dnsupdate
%_sbindir/samba_spnupdate
%_sbindir/samba_upgradedns
%dir /var/lib/samba/sysvol
%_datadir/samba/setup
%_man8dir/samba.8*
%_man8dir/samba-tool.8*
%else
%doc README.dc
%exclude %_man8dir/samba.8*
%exclude %_man8dir/samba-tool.8*
%endif
%if_with libcephfs
%exclude %_samba_mod_libdir/vfs/ceph.so
%exclude %_man8dir/vfs_ceph.8*
%endif
%if_enabled glusterfs
%exclude %_samba_mod_libdir/vfs/glusterfs.so
%exclude %_man8dir/vfs_glusterfs.8*
%endif

%files client
%_bindir/cifsdd
%_bindir/dbwrap_tool
%_bindir/nmblookup
%_bindir/oLschema2ldif
%_bindir/regdiff
%_bindir/regpatch
%_bindir/regshell
%_bindir/regtree
%_bindir/rpcclient
%_bindir/samba-regedit
%_bindir/sharesec
%_bindir/smbcacls
%_bindir/smbclient
%_bindir/smbcquotas
%_bindir/smbget
%_bindir/smbpasswd
%_bindir/smbprint
%_bindir/smbspool
#_bindir/smbta-util
%_bindir/smbtar
%_bindir/smbtree
%_libexecdir/samba/smbspool_krb5_wrapper
%{cups_serverbin}/backend/smb
%_man1dir/dbwrap_tool.1*
%_man1dir/nmblookup.1*
%_man1dir/oLschema2ldif.1*
%_man1dir/regdiff.1*
%_man8dir/samba-regedit.8*
%_man1dir/regpatch.1*
%_man1dir/regshell.1*
%_man1dir/regtree.1*
%exclude %_man1dir/findsmb.1*
%_man1dir/log2pcap.1*
%_man1dir/rpcclient.1*
%_man1dir/sharesec.1*
%_man1dir/smbcacls.1*
%_man1dir/smbclient.1*
%_man1dir/smbcquotas.1*
%_man1dir/smbget.1*
%_man5dir/smbgetrc.5*
%exclude %_man1dir/smbtar.1*
%_man1dir/smbtree.1*
%_man8dir/smbpasswd.8*
%_man8dir/smbspool.8*
%_man8dir/smbspool_krb5_wrapper.8*
#_man8dir/smbta-util.8*
%_man8dir/cifsdd.8*

%if_with ntdb
%_bindir/ntdbbackup
%_bindir/ntdbdump
%_bindir/ntdbrestore
%_bindir/ntdbtool
%_man3dir/ntdb.3*
%_man8dir/ntdbbackup.8*
%_man8dir/ntdbdump.8*
%_man8dir/ntdbrestore.8*
%_man8dir/ntdbtool.8*
%endif
%if_with tdb
%_bindir/tdbbackup
%_bindir/tdbdump
%_bindir/tdbrestore
%_bindir/tdbtool
%_man8dir/tdbbackup.8*
%_man8dir/tdbdump.8*
%_man8dir/tdbrestore.8*
%_man8dir/tdbtool.8*
%endif

%if_with ldb
%_bindir/ldbadd
%_bindir/ldbdel
%_bindir/ldbedit
%_bindir/ldbmodify
%_bindir/ldbrename
%_bindir/ldbsearch
%_man1dir/ldbadd.1*
%_man1dir/ldbdel.1*
%_man1dir/ldbedit.1*
%_man1dir/ldbmodify.1*
%_man1dir/ldbrename.1*
%_man1dir/ldbsearch.1*
%_samba_mod_libdir/libldb-cmdline.so
%endif

%files common -f net.lang
%_tmpfilesdir/%rname.conf
%_bindir/net
%_bindir/pdbedit
%_bindir/profiles
%_bindir/smbcontrol
%_bindir/testparm
%config(noreplace) %_sysconfdir/logrotate.d/samba
%attr(0700,root,root) %dir /var/log/samba
%attr(0700,root,root) %dir /var/log/samba/old
%dir /var/run/samba
%dir /var/run/winbindd
%attr(755,root,root) %dir %_localstatedir/cache/samba
%attr(700,root,root) %dir /var/lib/samba/private
%attr(755,root,root) %dir %_sysconfdir/samba
%config(noreplace) %_sysconfdir/samba/smb.conf
%config(noreplace) %_sysconfdir/samba/lmhosts
%config(noreplace) %_sysconfdir/sysconfig/samba
%_man1dir/profiles.1*
%_man1dir/smbcontrol.1*
%_man1dir/testparm.1*
%_man5dir/lmhosts.5*
%_man5dir/smb.conf.5*
%_man5dir/smbpasswd.5*
%_man7dir/samba.7*
%_man8dir/net.8*
%_man8dir/pdbedit.8*

# common libraries
%_samba_mod_libdir/libpopt-samba3-samba4.so
%_samba_mod_libdir/pdb

%files devel
%_includedir/samba-4.0

%exclude %_includedir/samba-4.0/netapi.h
%exclude %_includedir/samba-4.0/private
#%exclude %_includedir/samba-4.0/torture.h
%if_with libsmbclient
%exclude %_includedir/samba-4.0/libsmbclient.h
%endif
%if_with libwbclient
%exclude %_includedir/samba-4.0/wbclient.h
%endif

%_samba_libdir/libdcerpc-binding.so
%_samba_libdir/libdcerpc-samr.so
%_samba_libdir/libdcerpc.so
%_samba_libdir/libndr-krb5pac.so
%_samba_libdir/libndr-nbt.so
%_samba_libdir/libndr-standard.so
%_samba_libdir/libndr.so
%_samba_libdir/libsamba-credentials.so
%_samba_libdir/libsamba-errors.so
%_samba_libdir/libsamba-hostconfig.so
%_samba_libdir/libsamba-policy.so
%_samba_libdir/libsamba-util.so
%_samba_libdir/libsamdb.so
%_samba_libdir/libsmbconf.so
%_samba_libdir/libtevent-util.so
%_samba_libdir/libsamba-passdb.so
%_samba_libdir/libsmbldap.so

%_pkgconfigdir/dcerpc.pc
%_pkgconfigdir/dcerpc_samr.pc
%_pkgconfigdir/ndr.pc
%_pkgconfigdir/ndr_krb5pac.pc
%_pkgconfigdir/ndr_nbt.pc
%_pkgconfigdir/ndr_standard.pc
%_pkgconfigdir/samba-credentials.pc
%_pkgconfigdir/samba-hostconfig.pc
%_pkgconfigdir/samba-policy.pc
%_pkgconfigdir/samba-util.pc
%_pkgconfigdir/samdb.pc

%if_with dc
%_samba_libdir/libdcerpc-server.so
%_pkgconfigdir/dcerpc_server.pc
%endif

%files libs
%_samba_libdir/libdcerpc-binding.so.*
%_samba_libdir/libdcerpc-samr.so.*
%_samba_libdir/libdcerpc.so.*
%_samba_libdir/libndr-krb5pac.so.*
%_samba_libdir/libndr-nbt.so.*
%_samba_libdir/libndr-standard.so.*
%_samba_libdir/libndr.so.*
%_samba_libdir/libsamba-credentials.so.*
%_samba_libdir/libsamba-errors.so.*
%_samba_libdir/libsamba-hostconfig.so.*
%_samba_libdir/libsamba-policy.so.*
%_samba_libdir/libsamba-util.so.*
%_samba_libdir/libsamdb.so.*
%_samba_libdir/libsmbconf.so.*
%_samba_libdir/libtevent-util.so.*
%_samba_libdir/libsamba-passdb.so.*
%_samba_libdir/libsmbldap.so.*
%_samba_mod_libdir/auth
%_samba_mod_libdir/vfs

# libraries needed by the public libraries
%_samba_mod_libdir/libCHARSET3-samba4.so
%_samba_mod_libdir/libMESSAGING-samba4.so
%_samba_mod_libdir/libLIBWBCLIENT-OLD-samba4.so
%_samba_mod_libdir/libaddns-samba4.so
%_samba_mod_libdir/libads-samba4.so
%_samba_mod_libdir/libasn1util-samba4.so
%_samba_mod_libdir/libauth-samba4.so
%_samba_mod_libdir/libauth4-samba4.so
%_samba_mod_libdir/libauth-sam-reply-samba4.so
%_samba_mod_libdir/libauth-unix-token-samba4.so
%_samba_mod_libdir/libauthkrb5-samba4.so
%_samba_mod_libdir/libcli-ldap-common-samba4.so
%_samba_mod_libdir/libcli-ldap-samba4.so
%_samba_mod_libdir/libcli-nbt-samba4.so
%_samba_mod_libdir/libcli-cldap-samba4.so
%_samba_mod_libdir/libcli-smb-common-samba4.so
%_samba_mod_libdir/libcli-spoolss-samba4.so
%_samba_mod_libdir/libcliauth-samba4.so
%_samba_mod_libdir/libcluster-samba4.so
%_samba_mod_libdir/libcmdline-credentials-samba4.so
%_samba_mod_libdir/libdbwrap-samba4.so
%_samba_mod_libdir/libdcerpc-samba-samba4.so
%_samba_mod_libdir/libdcerpc-samba4.so
%_samba_mod_libdir/libevents-samba4.so
%_samba_mod_libdir/libflag-mapping-samba4.so
%_samba_mod_libdir/libgenrand-samba4.so
%_samba_mod_libdir/libgensec-samba4.so
%_samba_mod_libdir/libgpo-samba4.so
%_samba_mod_libdir/libgse-samba4.so
%_samba_mod_libdir/libhttp-samba4.so
%_samba_mod_libdir/libinterfaces-samba4.so
%_samba_mod_libdir/libiov-buf-samba4.so
%_samba_mod_libdir/libkrb5samba-samba4.so
%_samba_mod_libdir/libldbsamba-samba4.so
%_samba_mod_libdir/liblibcli-lsa3-samba4.so
%_samba_mod_libdir/liblibcli-netlogon3-samba4.so
%_samba_mod_libdir/liblibsmb-samba4.so
%_samba_mod_libdir/libmessages-dgm-samba4.so
%_samba_mod_libdir/libmessages-util-samba4.so
%_samba_mod_libdir/libmsghdr-samba4.so
%_samba_mod_libdir/libsmb-transport-samba4.so
%_samba_mod_libdir/libmsrpc3-samba4.so
%_samba_mod_libdir/libndr-samba-samba4.so
%_samba_mod_libdir/libndr-samba4.so
%_samba_mod_libdir/libnet-keytab-samba4.so
%_samba_mod_libdir/libnetif-samba4.so
%_samba_mod_libdir/libnon-posix-acls-samba4.so
%_samba_mod_libdir/libnpa-tstream-samba4.so
%_samba_mod_libdir/libprinting-migrate-samba4.so
%_samba_mod_libdir/libregistry-samba4.so
%_samba_mod_libdir/libreplace-samba4.so
%_samba_mod_libdir/libsamba-cluster-support-samba4.so
%_samba_mod_libdir/libsamba-debug-samba4.so
%_samba_mod_libdir/libsamba-modules-samba4.so
%_samba_mod_libdir/libsamba-net-samba4.so
%_samba_mod_libdir/libsamba-security-samba4.so
%_samba_mod_libdir/libsamba-sockets-samba4.so
%_samba_mod_libdir/libsamba-python-samba4.so
%_samba_mod_libdir/libsamdb-common-samba4.so
%_samba_mod_libdir/libsecrets3-samba4.so
%_samba_mod_libdir/libserver-id-db-samba4.so
%_samba_mod_libdir/libserver-role-samba4.so
%_samba_mod_libdir/libshares-samba4.so
%_samba_mod_libdir/libsamba3-util-samba4.so
%_samba_mod_libdir/libsmbclient-raw-samba4.so
%_samba_mod_libdir/libsmbd-base-samba4.so
%_samba_mod_libdir/libsmbd-conn-samba4.so
%_samba_mod_libdir/libsmbd-shim-samba4.so
%_samba_mod_libdir/libsmbldaphelper-samba4.so
%_samba_mod_libdir/libsmbpasswdparser-samba4.so
%_samba_mod_libdir/libsmbregistry-samba4.so
%_samba_mod_libdir/libsys-rw-samba4.so
%_samba_mod_libdir/libsocket-blocking-samba4.so
%_samba_mod_libdir/libtalloc-report-samba4.so
%_samba_mod_libdir/libtdb-wrap-samba4.so
%_samba_mod_libdir/libtime-basic-samba4.so
%_samba_mod_libdir/libtorture-samba4.so
%_samba_mod_libdir/libtrusts-util-samba4.so
%_samba_mod_libdir/libutil-cmdline-samba4.so
%_samba_mod_libdir/libutil-reg-samba4.so
%_samba_mod_libdir/libutil-setid-samba4.so
%_samba_mod_libdir/libutil-tdb-samba4.so
%_samba_mod_libdir/libxattr-tdb-samba4.so

%if_with dc
%_samba_mod_libdir/bind9/dlz_bind9.so
%_samba_mod_libdir/bind9/dlz_bind9_9.so
%_samba_mod_libdir/bind9/dlz_bind9_10.so
%_samba_mod_libdir/bind9/dlz_bind9_11.so
%_samba_mod_libdir/libheimntlm-samba4.so.1
%_samba_mod_libdir/libheimntlm-samba4.so.1.0.1
%_samba_mod_libdir/libkdc-samba4.so.2
%_samba_mod_libdir/libkdc-samba4.so.2.0.0
%_samba_mod_libdir/libpac-samba4.so
%_samba_mod_libdir/libdnsserver-common-samba4.so
%_samba_mod_libdir/libdfs-server-ad-samba4.so
%_samba_mod_libdir/libdsdb-module-samba4.so
%_samba_mod_libdir/ldb
%_samba_mod_libdir/gensec
%_samba_mod_libdir/libdb-glue-samba4.so
%_samba_mod_libdir/libHDB-SAMBA4-samba4.so
%_samba_mod_libdir/libasn1-samba4.so.*
%_samba_mod_libdir/libcom_err-samba4.so.*
%_samba_mod_libdir/libgssapi-samba4.so.*
%_samba_mod_libdir/libhcrypto-samba4.so.*
%_samba_mod_libdir/libhdb-samba4.so.*
%_samba_mod_libdir/libheimbase-samba4.so.*
%_samba_mod_libdir/libhx509-samba4.so.*
%_samba_mod_libdir/libkrb5-samba4.so.*
%_samba_mod_libdir/libroken-samba4.so.*
%_samba_mod_libdir/libwind-samba4.so.*
%_samba_mod_libdir/libprocess-model-samba4.so
%_samba_mod_libdir/libservice-samba4.so
%_samba_mod_libdir/process_model
%_samba_mod_libdir/service
%_samba_libdir/libdcerpc-server.so.*
%if_with ntvfs
%_samba_mod_libdir/libntvfs-samba4.so
%endif
%_samba_mod_libdir/libposix-eadb-samba4.so
%else
%doc README.dc-libs
%_samba_mod_libdir/libdnsserver-common-samba4.so
%endif

%if_with ldb
%_samba_mod_libdir/libldb.so.*
%_samba_mod_libdir/libpyldb-util.so.*
%endif
%if_with talloc
%_samba_mod_libdir/libtalloc.so.*
%_samba_mod_libdir/libpytalloc-util.so.*
%endif
%if_with tevent
%_samba_mod_libdir/libtevent.so.*
%endif
%if_with tdb
%_samba_mod_libdir/libtdb.so.*
%endif
%if_with ntdb
%_samba_mod_libdir/libntdb.so.*
%endif
%if_without libsmbclient
%_samba_mod_libdir/libsmbclient.so.*
%endif
%if_without libwbclient
%_samba_mod_libdir/libwbclient.so.*
%_samba_mod_libdir/libwinbind-client-samba4.so
%endif
%if_without libnetapi
%_samba_mod_libdir/libnetapi.so.*
%endif

%if_with libsmbclient
%files -n libsmbclient-DC
%_samba_libdir/libsmbclient.so.*

%files -n libsmbclient-DC-devel
%_includedir/samba-4.0/libsmbclient.h
%_samba_libdir/libsmbclient.so
%_pkgconfigdir/smbclient.pc
%_man7dir/libsmbclient.7*
%endif

%if_with libwbclient
%files -n libwbclient-DC
%_samba_libdir/libwbclient.so.*
%_samba_mod_libdir/libwinbind-client-samba4.so

%files -n libwbclient-DC-devel
%_includedir/samba-4.0/wbclient.h
%_samba_libdir/libwbclient.so
%_pkgconfigdir/wbclient.pc
%endif

%if_with libnetapi
%files -n libnetapi-DC
%_samba_libdir/libnetapi.so.*

%files -n libnetapi-DC-devel
%_samba_libdir/libnetapi.so
%_includedir/samba-4.0/netapi.h
%_pkgconfigdir/netapi.pc
%endif

%files pidl
%attr(755,root,root) %_bindir/pidl
%_man1dir/pidl.1.*
%_man3dir/Parse::Pidl::*
%perl_vendor_privlib/*

%files -n python-module-%name
%python_sitelibdir/*

%if_with docs
%files doc
%doc %_defaultdocdir/%rname/htmldocs
%endif

%files test
%_bindir/gentest
%_bindir/locktest
%_bindir/masktest
%_bindir/ndrdump
%_bindir/smbtorture
#%_samba_libdir/libtorture.so.*
%if_with dc
%_samba_mod_libdir/libdlz-bind9-for-torture-samba4.so
%else
%_samba_mod_libdir/libdsdb-module-samba4.so
%endif
%_man1dir/gentest.1*
%_man1dir/locktest.1*
%_man1dir/masktest.1*
%_man1dir/ndrdump.1*
%_man1dir/smbtorture.1*
%_man1dir/vfstest.1*

%if_with testsuite
# files to ignore in testsuite mode
%_samba_mod_libdir/libnss-wrapper-samba4.so
%_samba_mod_libdir/libsocket-wrapper-samba4.so
%_samba_mod_libdir/libuid-wrapper-samba4.so
%endif

%if_with winbind
%files winbind -f pam_winbind.lang
%_samba_mod_libdir/idmap
%_samba_mod_libdir/nss_info
%_samba_mod_libdir/libnss-info-samba4.so
%_samba_mod_libdir/libidmap-samba4.so
%_sbindir/winbindd
%attr(750,root,wbpriv) %dir /var/lib/samba/winbindd_privileged
%_unitdir/winbind.service
%attr(755,root,root) %_initrddir/winbind
%_sysconfdir/NetworkManager/dispatcher.d/30-winbind
%_man8dir/winbindd.8*
%_man8dir/idmap_*.8*

%files winbind-clients
%_bindir/ntlm_auth
%_bindir/wbinfo
%_samba_libdir/libnss_winbind.so*
/%_lib/libnss_winbind.so.*
%_samba_libdir/libnss_wins.so*
/%_lib/libnss_wins.so.*
/%_lib/security/pam_winbind.so
%config(noreplace) %_sysconfdir/security/pam_winbind.conf
%_man1dir/ntlm_auth.1.*
%_man1dir/wbinfo.1*
%_man5dir/pam_winbind.conf.5*
%_man8dir/pam_winbind.8*

%files winbind-krb5-locator
%_libdir/krb5/plugins/libkrb5/winbind_krb5_locator.so
%_man7dir/winbind_krb5_locator.7*
%endif

%if_with clustering_support
%files ctdb
#doc ctdb/README
%config(noreplace) %_sysconfdir/sysconfig/ctdb
%dir %_sysconfdir/ctdb
%config(noreplace) %_sysconfdir/ctdb/nodes
%config(noreplace) %_sysconfdir/ctdb/notify.sh
%config(noreplace) %_sysconfdir/ctdb/debug-hung-script.sh
%config(noreplace) %_sysconfdir/ctdb/ctdb-crash-cleanup.sh
%config(noreplace) %_sysconfdir/ctdb/gcore_trace.sh
%config(noreplace) %_sysconfdir/ctdb/functions
%config(noreplace) %_sysconfdir/ctdb/debug_locks.sh
%_sysconfdir/ctdb/statd-callout
%dir /var/lib/ctdb
%_unitdir/ctdb.service
%_initdir/ctdb
%_tmpfilesdir/ctdb.conf

%_sysconfdir/ctdb/nfs-checks.d
%_sysconfdir/ctdb/nfs-linux-kernel-callout
%_sysconfdir/sudoers.d/ctdb
%_sysconfdir/ctdb/events.d
%dir %_sysconfdir/ctdb/notify.d
%_sysconfdir/ctdb/notify.d/README
%_sbindir/ctdbd
%_sbindir/ctdbd_wrapper
%_bindir/ctdb
%_bindir/ctdb_diagnostics
%_bindir/ltdbtool
%_bindir/onnode
%_bindir/ping_pong
%_libexecdir/ctdb/ctdb_event_helper
%_libexecdir/ctdb/ctdb_lock_helper
%_libexecdir/ctdb/ctdb_natgw
%_libexecdir/ctdb/ctdb_recovery_helper
%_libexecdir/ctdb/smnotify

%_man1dir/ctdb.1*
%_man1dir/ctdbd.1*
%_man1dir/onnode.1*
%_man1dir/ltdbtool.1*
%_man1dir/ping_pong.1*
%_man1dir/ctdbd_wrapper.1*
%_man5dir/ctdbd.conf.5*
%_man7dir/ctdb.7*
%_man7dir/ctdb-tunables.7*
%_man7dir/ctdb-statistics.7*

%files ctdb-tests
%_libexecdir/ctdb/tests
%_bindir/ctdb_run_tests
%_bindir/ctdb_run_cluster_tests
%_datadir/ctdb/tests
%endif

%files -n task-samba-dc

%files util-private-headers
%_includedir/samba-4.0/private

%changelog
* Thu May 25 2017 Evgeny Sinelnikov <sin@altlinux.ru> 4.4.14-alt0.M70C.1
- Update with latest security fixes:
  + CVE-2016-2123 Fix DNS vuln ZDI-CAN-3995
  + CVE-2016-2125 Unconditional privilege delegation to Kerberos servers in
    trusted realms
  + CVE-2016-2126 Flaws in Kerberos PAC validation can trigger privilege
    elevation
  + CVE-2017-2619 Symlink race allows access outside share definition
  + CVE-2017-7494 Remote code execution from a writable share

* Sat Jul 09 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.5-alt0.M70C.1
- [backport] Update for security release with CVE-2016-2119

* Thu Jun 30 2016 Evgeny Sinelnikov <sin@altlinux.ru> 4.4.4-alt3
- Apply fixes for DRSUAPI limits of too strict for some workloads,
  e.g. DRSUAPI replication with large objects.
   https://bugzilla.samba.org/show_bug.cgi?id=11948
 + Set DCERPC_NCACN_{REQUEST,RESPONSE}_DEFAULT_MAX_SIZE
 + Allow a total reassembled response payload of 240 MBytes

* Wed Jun 29 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.4-alt2
- Package libsamba_util private headers to package
  samba-DC-util-private-headers

* Fri Jun 10 2016 Evgeny Sinelnikov <sin@altlinux.ru> 4.4.4-alt1
- Update to new version

* Tue May 24 2016 Alexey Shabalin <shaba@altlinux.ru> 4.4.3-alt3
- build with libsystemd without compat libs
- add patches from fedora
- add again samba-grouppwd.patch

* Mon May 23 2016 Evgeny Sinelnikov <sin@altlinux.ru> 4.4.3-alt2
- Fix rpc_server/drsuapi: Set msDS_IntId as attid for linked attributes if exists

* Wed May 04 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.3-alt0.M70C.1
- Backport new version to p7 branch

* Wed May 04 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.3-alt1
- New version

* Mon May 02 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.2-alt1.M70C.1
- Fix CVE-2016-2110/NTLMSSP regression (https://bugzilla.samba.org/show_bug.cgi?id=11849)

* Tue Apr 12 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.2-alt0.M70C.1
- New version
- Security fixes:
  - CVE-2015-5370 (Multiple errors in DCE-RPC code)
  - CVE-2016-2110 (Man in the middle attacks possible with NTLMSSP)
  - CVE-2016-2111 (NETLOGON Spoofing Vulnerability)
  - CVE-2016-2112 (LDAP client and server don't enforce integrity)
  - CVE-2016-2113 (Missing TLS certificate validation)
  - CVE-2016-2114 ("server signing = mandatory" not enforced)
  - CVE-2016-2115 (SMB IPC traffic is not integrity protected)
  - CVE-2016-2118 (SAMR and LSA man in the middle attacks possible)

* Wed Mar 23 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.0-alt0.M70P.1
- Backport new version to p7 branch

* Tue Mar 22 2016 Andrey Cherepanov <cas@altlinux.org> 4.4.0-alt1
- New version (https://www.samba.org/samba/history/samba-4.4.0.html)
- Remove samba-DC-test-build and samba-DC-ctdb-devel

* Sun Mar 13 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.6-alt1.M70P.1
- Rebuild with downgraded libtalloc (ALT #31881)

* Sun Mar 13 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.6-alt2
- Rebuild with new libtalloc

* Wed Mar 09 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.6-alt0.M70P.1
- Backport new version to p7 branch

* Wed Mar 09 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.6-alt1
- New version (https://www.samba.org/samba/history/samba-4.3.6.html)
- Security fixes:
  - CVE-2015-7560 (Incorrect ACL get/set allowed on symlink path)
  - CVE-2016-0771 (Out-of-bounds read in internal DNS server)
- Do not use specified GID for wbpriv group

* Fri Mar 04 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.5-alt0.M70P.1
- Backport new version to p7 branch

* Thu Mar 03 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.5-alt1
- New version (https://www.samba.org/samba/history/samba-4.3.5.html)

* Thu Jan 14 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.4-alt0.M70P.1
- Backport new version to p7 branch

* Tue Jan 12 2016 Andrey Cherepanov <cas@altlinux.org> 4.3.4-alt1
- New version (https://www.samba.org/samba/history/samba-4.3.4.html)

* Thu Dec 24 2015 Andrey Cherepanov <cas@altlinux.org> 4.3.3-alt1.M70P.1
- Change services type from notify to forking

* Sat Dec 19 2015 Andrey Cherepanov <cas@altlinux.org> 4.3.3-alt0.M70P.2
- Backport new version with security fixes from Sisyphus to p7 branch

* Wed Dec 16 2015 Andrey Cherepanov <cas@altlinux.org> 4.3.3-alt0.M70C.1
- New version (https://www.samba.org/samba/history/samba-4.3.3.html)
- Security fixes:
  - CVE-2015-3223 (Denial of service in Samba Active Directory
  server)
  - CVE-2015-5252 (Insufficient symlink verification in smbd)
  - CVE-2015-5299 (Missing access control check in shadow copy
  code)
  - CVE-2015-5296 (Samba client requesting encryption vulnerable
  to downgrade attack)
  - CVE-2015-8467 (Denial of service attack against Windows
  Active Directory server)
  - CVE-2015-5330 (Remote memory read in Samba LDAP server)

* Tue Sep 22 2015 Andrey Cherepanov <cas@altlinux.org> 4.3.0-alt1.M70C.1
- Backport to c7 branch
