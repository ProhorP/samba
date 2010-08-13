%define samba4_version 4.0.0
%define pre_release alpha11
%define main_release 24

# Most of these subpackages are disabled because they are not
# needed by OpenChange, and to avoid file conflicts with Samba3.
%def_disable samba4
%def_disable client
%def_disable common
%def_disable python
%def_disable winbind

# Install libraries not needed by OpenChange.
%define all_libraries  0

Name: samba4
Version: %samba4_version
Release: alt1.%pre_release
Group: System/Servers
Summary: The Samba4 CIFS and AD client and server suite
License: GPLv3+ and LGPLv3+
Url: http://www.samba.org/
Packager: Alexey Shabalin <shaba@altlinux.ru>

Source: %name-%version.tar

# Red Hat specific replacement-files
Source1: %name.log
Source4: %name.sysconfig
Source5: %name.init

Patch1: samba-4.0.0alpha6-GIT-3508a66-undefined-comparison_fn_t.patch

%if_enabled common
Requires(pre): %name-common = %version-%release
%endif

BuildRequires: libe2fs-devel
BuildRequires: libacl-devel
BuildRequires: libaio-devel
BuildRequires: libattr-devel
BuildRequires: libncurses-devel
BuildRequires: libpam-devel
BuildRequires: perl-devel
BuildRequires: perl-Parse-Yapp
BuildRequires: libpopt-devel
BuildRequires: python-devel
BuildRequires: libreadline-devel
BuildRequires: libldap-devel
BuildRequires: libxslt xsltproc
BuildRequires: docbook-style-xsl

BuildRequires: libtalloc-devel, libtdb-devel, libtevent-devel, libldb-devel

%description
Samba 4 is the ambitious next version of the Samba suite that is being
developed in parallel to the stable 3.0 series. The main emphasis in
this branch is support for the Active Directory logon protocols used
by Windows 2000 and above.

%package client
Summary: Samba client programs
Group: Networking/Other
Requires: %name-common = %version-%release
Requires: %name-libs = %version-%release

%description client
The %name-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.

%package libs
Summary: Samba libraries
Group: System/Libraries

%description libs
The %name-libs package contains the libraries needed by programs that
link against the SMB, RPC and other protocols provided by the Samba suite.

%package -n python-module-%name
Summary: Samba Python libraries
Group: Networking/Other
Requires: %name-libs = %version-%release

%add_python_req_skip Tdb

%description -n python-module-%name
The %name-python package contains the Python libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python programs.

%package devel
Summary: Developer tools for Samba libraries
Group: Development/C
Requires: %name-libs = %version-%release

%description devel
The %name-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.

%package pidl
Summary: Perl IDL compiler
Group: Development/Tools
# Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description pidl
The %name-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols

%package common
Summary: Files used by both Samba servers and clients
Group: System/Servers
Requires: %name-libs = %version-%release

%description common
%name-common provides files necessary for both the server and client
packages of Samba.

%package winbind
Summary: Samba winbind
Group: System/Servers
Requires: %name = %version-%release

%description winbind
The samba-winbind package provides the winbind NSS library, and some
client tools.  Winbind enables Linux to be a full member in Windows
domains and to use Windows user and group accounts on Linux.

%prep
%setup -q

# copy Red Hat specific scripts

%patch1 -p1 -b .undefined-comparison_fn_t

mv source4/VERSION source4/VERSION.orig
sed -e 's/SAMBA_VERSION_VENDOR_SUFFIX=$/&%main_release/' < source4/VERSION.orig > source4/VERSION
#cd source4
#script/mkversion.sh
#cd ..

%build

cd source4
./autogen.sh

%configure \
	--enable-fhs \
	--with-lockdir=/var/lib/%name \
	--with-piddir=/var/run \
	--with-privatedir=/var/lib/%name/private \
	--with-logfilebase=/var/log/%name \
	--sysconfdir=%_sysconfdir/%name \
	--with-winbindd-socket-dir=/var/run/winbind \
	--with-ntp-signd-socket-dir=/var/run/ntp_signd \
	--disable-gnutls

# Build PIDL for installation into vendor directories before
# 'make proto' gets to it.
(cd ../pidl && perl Makefile.PL INSTALLDIRS=vendor )

# Builds using PIDL the IDL and many other things.
#make proto
#make everything
make

%install
cd source4

# Don't call 'make install' as we want to call out to the PIDL
# install manually.
make install DESTDIR=%buildroot

# Undo the PIDL install, we want to try again with the right options.
rm -rf %buildroot%_libdir/perl5
rm -rf %buildroot%_datadir/perl5

# Install PIDL.
( cd ../pidl && make install PERL_INSTALL_ROOT=%buildroot )

# Clean out crap left behind by the PIDL install.
find %buildroot -type f -name .packlist -exec rm -f {} \;
find %buildroot -depth -type d -exec rmdir {} 2>/dev/null \;

cd ..

%if_enabled samba4
mkdir -p %buildroot%_initdir
mkdir -p %buildroot%_sysconfdir/logrotate.d
mkdir -p %buildroot%_sysconfdir/sysconfig
%endif

mkdir -p %buildroot/var/run/winbindd
mkdir -p %buildroot/var/run/ntp_signd
mkdir -p %buildroot/var/lib/%name/winbindd_privileged
mkdir -p %buildroot/var/log/%name/
mkdir -p %buildroot/var/log/%name/old

mkdir -p %buildroot/var/lib/%name
mkdir -p %buildroot/var/lib/%name/private
mkdir -p %buildroot/var/lib/%name/sysvol

mkdir -p %buildroot%_sysconfdir/%name

%if_enabled samba4
# Install other stuff.
install -m755 %SOURCE5 %buildroot%_initdir/%name
install -m644 %SOURCE1 %buildroot%_sysconfdir/logrotate.d/%name
install -m644 %SOURCE4 %buildroot%_sysconfdir/sysconfig/%name
%endif

%if_enabled winbind
mkdir -p %buildroot%_lib
ln -sf ../%_libdir/libnss_winbind.so  %buildroot%_lib/libnss_winbind.so.2
%else
rm %buildroot%_bindir/ntlm_auth
rm %buildroot%_bindir/wbinfo
rm %buildroot%_libdir/libnss_winbind.so
%endif

# libs {
mkdir -p %buildroot%_libdir %buildroot%_includedir

# }

# Clean out some stuff we don't want in package.
# rm %buildroot%_bindir/mount.cifs
# rm %buildroot%_bindir/umount.cifs

#rm %buildroot%_bindir/epdump
rm %buildroot%_bindir/gentest
rm %buildroot%_bindir/getntacl
rm %buildroot%_bindir/locktest
rm %buildroot%_bindir/masktest
#rm %buildroot%_bindir/minschema
rm %buildroot%_bindir/ndrdump
rm %buildroot%_bindir/nsstest
rm %buildroot%_bindir/setnttoken
rm %buildroot%_bindir/smbtorture
#rm %buildroot%_bindir/subunitrun
#depending on the environemnt this file might or might not be generated
rm -f %buildroot%_bindir/tdbtorture

# Avoids a file conflict with perl-Parse-Yapp.
rm -rf %buildroot%perl_vendor_privlib/Parse/Yapp

# Remove files for disabled subpackages.
%if_disabled samba4
#rm %buildroot%_bindir/mymachinepw
rm %buildroot%_sbindir/provision
rm %buildroot%_sbindir/samba
rm %buildroot%_sbindir/upgradeprovision
rm -r %buildroot%_datadir/samba/setup
%endif
%if_enabled client
# Fix *mount.cifs
mkdir -p %buildroot/sbin
mv %buildroot%_bindir/*mount.cifs %buildroot/sbin/
ln -s ../../sbin/mount.cifs %buildroot%_bindir/cifsmount
ln -s ../../sbin/umount.cifs %buildroot%_bindir/cifsumount
%endif

%if_disabled client
rm %buildroot%_bindir/nmblookup
rm %buildroot%_bindir/smbclient
rm %buildroot%_bindir/cifsdd
%endif
%if_disabled common
rm %buildroot%_bindir/net
rm %buildroot%_bindir/regdiff
rm %buildroot%_bindir/regpatch
rm %buildroot%_bindir/regshell
rm %buildroot%_bindir/regtree
rm %buildroot%_bindir/testparm
%endif
%if_disabled all_libraries
rm %buildroot%_libdir/libdcerpc_atsvc.so
rm %buildroot%_libdir/libdcerpc_atsvc.so.*
rm %buildroot%_libdir/libgensec.so
rm %buildroot%_libdir/libgensec.so.*
rm %buildroot%_libdir/libregistry.so
rm %buildroot%_libdir/libregistry.so.*
rm %buildroot%_libdir/libtorture.so
rm %buildroot%_libdir/libtorture.so.*
rm %buildroot%_pkgconfigdir/dcerpc_atsvc.pc
rm %buildroot%_pkgconfigdir/gensec.pc
rm %buildroot%_pkgconfigdir/registry.pc
rm %buildroot%_pkgconfigdir/torture.pc
rm %buildroot%_includedir/samba-4.0/gensec.h
rm %buildroot%_includedir/samba-4.0/registry.h
%endif

# the samba4 build process rebuilds libraries internally,
# but we want to use the standalone build for now.
rm %buildroot%_libdir/libldb.so*
#rm %buildroot%_bindir/ad2oLschema
rm %buildroot%_bindir/ldbadd
rm %buildroot%_bindir/ldbdel
rm %buildroot%_bindir/ldbedit
rm %buildroot%_bindir/ldbmodify
rm %buildroot%_bindir/ldbrename
rm %buildroot%_bindir/ldbsearch
rm %buildroot%_bindir/oLschema2ldif
rm -f %buildroot%_bindir/tdbbackup
rm -f %buildroot%_bindir/tdbdump
rm -f %buildroot%_bindir/tdbtool

rm -f %buildroot%_libdir/lib*.a

%if_disabled python
rm -r %buildroot%python_sitelibdir/*
rm -fr %buildroot%python_libdir/lib
%endif

# These may be created in non mock systems, but we do not want to package them
# for now
rm -f %buildroot%_man1dir/ad2oLschema.1
rm -f %buildroot%_man1dir/oLschema2ldif.1
rm -f %buildroot%_datadir/swig/*/talloc.i

# This makes the right links, as rpmlint requires that
# the ldconfig-created links be recorded in the RPM.
#   /sbin/ldconfig -N -n %buildroot%_libdir

# Fix up permission on perl install.
%_fixperms %buildroot%perl_vendor_privlib

# Fix up permissions in source tree, for debuginfo.
find source4/heimdal -type f | xargs chmod -x

%pre
%if_enabled winbind
getent group wbpriv >/dev/null || groupadd -g 88 wbpriv
%endif
exit 0

%post
%if_enabled samba4
/sbin/chkconfig --add %name
if [ "$1" -ge "1" ]; then
	/sbin/service %name condrestart >/dev/null 2>&1 || :
fi
%endif
exit 0

%preun
%if_enabled samba4
if [ $1 = 0 ] ; then
	/sbin/service %name stop >/dev/null 2>&1 || :
	/sbin/chkconfig --del %name
fi
%endif
exit 0

%files
%doc COPYING WHATSNEW4.txt
%if_enabled samba4
%_bindir/mymachinepw
%_bindir/smbstatus
%_sbindir/provision
%_sbindir/samba
%_sbindir/upgradeprovision
%_datadir/samba/setup
%dir /var/lib/%name/sysvol
%config(noreplace) %_sysconfdir/logrotate.d/%name
%config(noreplace) %_sysconfdir/sysconfig/%name
%attr(0755,root,root) %_initdir/%name
%attr(0700,root,root) %dir /var/log/%name
%attr(0700,root,root) %dir /var/log/%name/old
%endif

%files libs
%doc PFIF.txt
%dir %_datadir/samba
%_datadir/samba/*.dat
%_libdir/libdcerpc.so.*
%_libdir/libdcerpc_samr.so.*
%_libdir/libndr.so.*
%_libdir/libndr_standard.so.*
%_libdir/libsamba-hostconfig.so.*
%_libdir/libsamba-util.so.*
#%_libdir/libtorture.so.*
#Only needed if Samba's build produces plugins
#%_libdir/samba
%dir %_sysconfdir/%name
#Need to mark this as being owned by Samba, but it is normally created
#by the provision script, which runs best if there is no existing
#smb.conf
#%config(noreplace) %_sysconfdir/%name/smb.conf
%if_enabled all_libraries
%_libdir/libdcerpc_atsvc.so.*
%_libdir/libgensec.so.*
%_libdir/libregistry.so.*
%endif

%if_enabled winbind
%files winbind
%_bindir/ntlm_auth
%_bindir/wbinfo
%_libdir/libnss_winbind.so
/%_lib/libnss_winbind.so.2
%dir /var/run/winbindd
%attr(750,root,wbpriv) %dir /var/lib/%name/winbindd_privileged
%endif

%if_enabled python
%files -n python-module-%name
%python_sitelibdir/*
%python_libdir/lib
%endif

%files devel
%_includedir/samba-4.0
%_libdir/libdcerpc.so
%_libdir/libdcerpc_samr.so
%_libdir/libndr.so
%_libdir/libndr_standard.so
%_libdir/libsamba-hostconfig.so
%_libdir/libsamba-util.so
#%_libdir/libtorture.so
%_pkgconfigdir/dcerpc.pc
%_pkgconfigdir/dcerpc_samr.pc
%_pkgconfigdir/ndr.pc
%_pkgconfigdir/ndr_standard.pc
%_pkgconfigdir/samba-hostconfig.pc
#%_pkgconfigdir/torture.pc
%if_enabled all_libraries
%_libdir/libdcerpc_atsvc.so
%_libdir/libgensec.so
%_libdir/libregistry.so
%_pkgconfigdir/dcerpc_atsvc.pc
%_pkgconfigdir/gensec.pc
%_pkgconfigdir/registry.pc
%_includedir/samba-4.0/gen_ndr
%endif

%files pidl
%perl_vendor_privlib/*
%_man1dir/pidl*
%_man3dir/Parse*
%attr(755,root,root) %_bindir/pidl

%if_enabled client
%files client
/sbin/mount.cifs
/sbin/umount.cifs

%_bindir/nmblookup
%_bindir/smbclient
%_bindir/cifsdd

%_bindir/autoidl
%_bindir/epdump
%_bindir/gentest
%_bindir/getntacl
%_bindir/locktest
%_bindir/masktest
%_bindir/ndrdump
%_bindir/nsstest
%_bindir/rpcclient
%_bindir/samba3dump
%_bindir/setnttoken
%_bindir/smbtorture

%endif

%if_enabled common
%files common
%_bindir/net
%_bindir/testparm
%_bindir/regdiff
%_bindir/regpatch
%_bindir/regshell
%_bindir/regtree

%dir /var/lib/%name
%attr(700,root,root) %dir /var/lib/%name/private
# We don't want to put a smb.conf in by default, provision should create it
#%config(noreplace) %_sysconfdir/%name/smb.conf
%endif

%changelog
* Fri Aug 13 2010 Alexey Shabalin <shaba@altlinux.ru> 4.0.0-alt1.alpha11
- initial build for ALT Linux Sisyphus

* Mon Jun 28 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 4.0.0-24.alpha11
- Revert changes to %%Release, use %%main_release instead.
- Rebuild for perl-5.12.x.

* Mon Jun 28 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 4.0.0-23.alpha11.2
- Once again rebuild for perl-5.12.x.

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.0.0-23.alpha11.1
- Mass rebuild with perl-5.12.0

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 4.0.0-23.alpha11
- Rebuild against newer libtevent

* Sun Jan 24 2010 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-22.alpha11
- Upgrade to alpha11

* Fri Jan 08 2010 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-21.alpha10
- Bump ldb_version to 0.9.10.

* Fri Jan 08 2010 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-20.alpha10
- Only install new command-line utilities if enable_samba4 is non-zero.

* Wed Jan 06 2010 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-19.alpha10
- Upgrade to alpha10

* Thu Sep 17 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-18.1.alpha8_git20090916
- Need docbook stuff to build man pages

* Thu Sep 17 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-18.alpha8_git20090916
- Fix broken dependencies

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-17.alpha8_git20090916
- Upgrade to alpha8-git20090916

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-16.alpha7
- Stop building libtevent, it is now an external package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-15.2alpha7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-15.2alpha7
- Fix dependency

* Sat May 09 2009  Simo Sorce <ssorce@redhat.com> - 4.0.0-15.1alpha7
- Don't build talloc and tdb, they are now separate packages

* Mon Apr 06 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-14alpha7
- Fix a build issue in samba4-common (RH bug #494243).

* Wed Mar 25 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-13alpha7
- rebuild with correct CFLAGS (also fixes debuginfo)

* Tue Mar 10 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-12alpha7
- Second part of fix for the ldb segfault problem from upstream

* Mon Mar 09 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-11alpha7
- Add upstream patch to fix a problem within ldb

* Sun Mar 08 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-10alpha7
- Remove ldb.pc from samba4-devel (RH bug #489186).

* Wed Mar  4 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-9alpha7
- Make talloc,tdb,tevent,ldb easy to exclude using defines
- Fix package for non-mock "dirty" systems by deleting additional
  files we are not interested in atm

* Wed Mar  4 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-8alpha7
- Fix typo in Requires

* Mon Mar  2 2009 Simo Sorce <ssorce@redhat.com> - 4.0.0-7alpha7
- Compile and have separate packages for additional samba libraries
  Package in their own packages: talloc, tdb, tevent, ldb

* Fri Feb 27 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-4.alpha7
- Update to 4.0.0alpha7

* Wed Feb 25 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-3.alpha6
- Formal package review cleanups.

* Mon Feb 23 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-2.alpha6
- Disable subpackages not needed by OpenChange.
- Incorporate package review feedback.

* Mon Jan 19 2009 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-1.alpha6
- Update to 4.0.0alpha6

* Wed Dec 17 2008 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-0.8.alpha6.GIT.3508a66
- Fix another file conflict: smbstatus

* Fri Dec 12 2008 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-0.7.alpha6.GIT.3508a66
- Disable the winbind subpackage because it conflicts with samba-winbind
  and isn't needed to support OpenChange.

* Fri Dec 12 2008 Matthew Barnes <mbarnes@redhat.com> - 4.0.0-0.6.alpha6.GIT.3508a66
- Update to the GIT revision OpenChange is now requiring.

* Fri Aug 29 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.5.alpha5.fc10
- Fix licence tag (the binaries are built into a GPLv3 whole, so the BSD licence need not be mentioned)

* Fri Jul 25 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.4.alpha5.fc10
- Remove talloc and tdb dependency (per https://bugzilla.redhat.com/show_bug.cgi?id=453083)
- Fix deps on chkconfig and service to main pkg (not -common)
  (per https://bugzilla.redhat.com/show_bug.cgi?id=453083)

* Mon Jul 21 2008 Brad Hards <bradh@frogmouth.ent> - 0:4.0.0-0.3.alpha5.fc10
- Use --sysconfdir instead of --with-configdir
- Add patch for C++ header compatibility

* Mon Jun 30 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.2.alpha5.fc9
- Update per review feedback
- Update for alpha5

* Thu Jun 26 2008 Andrew Bartlett <abartlet@samba.org> - 0:4.0.0-0.1.alpha4.fc9
- Rework Fedora's Samba 3.2.0-1.rc2.16 spec file for Samba4
