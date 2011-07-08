%define tarball libX11
#define gitdate 20090805

Summary: Core X11 protocol client library
Name: libX11
Version: 1.3
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
#Source0: http://cgit.freedesktop.org/xorg/lib/libX11/snapshot/libX11-%{version}.tar.bz2 
#Source0:    %{tarball}-%{gitdate}.tar.bz2
#Source1:    make-git-snapshot.sh

Patch2: dont-forward-keycode-0.patch
Patch3: libX11-1.3.1-creategc-man-page.patch

BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: xorg-x11-util-macros
BuildRequires: pkgconfig(xproto) >= 7.0.15
BuildRequires: xorg-x11-xtrans-devel >= 1.0.3-4
BuildRequires: libxcb-devel >= 1.2
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel

Requires: %{name}-common = %{version}-%{release}

%description
Core X11 protocol client library.

%package common
Summary: Common data for libX11
Group: System Environment/Libraries
BuildArch: noarch

%description common
libX11 common data

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

Requires: libXau-devel, libXdmcp-devel
Requires: pkgconfig

%description devel
X.Org X11 libX11 development package

%prep
%setup -q
#setup -q -n %{tarball}-%{gitdate}
%patch2 -p1 -b .dont-forward-keycode-0
%patch3 -p1 -b .manual

%build
# sodding libtool
autoreconf -v --install
%configure \
	--disable-dependency-tracking \
	--disable-static

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# FIXME: Don't install Xcms.txt - find out why upstream still ships this.
find $RPM_BUILD_ROOT -name 'Xcms.txt' -delete

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libX11.so.6
%{_libdir}/libX11.so.6.3.0
%{_libdir}/libX11-xcb.so.1
%{_libdir}/libX11-xcb.so.1.0.0

%files common
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS
%dir %{_datadir}/X11
%{_datadir}/X11/locale/
%{_datadir}/X11/XErrorDB
%{_datadir}/X11/XKeysymDB

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/ImUtil.h
%{_includedir}/X11/XKBlib.h
%{_includedir}/X11/Xcms.h
%{_includedir}/X11/Xlib.h
%{_includedir}/X11/XlibConf.h
%{_includedir}/X11/Xlibint.h
%{_includedir}/X11/Xlib-xcb.h
%{_includedir}/X11/Xlocale.h
%{_includedir}/X11/Xregion.h
%{_includedir}/X11/Xresource.h
%{_includedir}/X11/Xutil.h
%{_includedir}/X11/cursorfont.h
%{_libdir}/libX11.so
%{_libdir}/libX11-xcb.so
%{_libdir}/pkgconfig/x11.pc
%{_libdir}/pkgconfig/x11-xcb.pc
%{_mandir}/man3/*.3*

%changelog
* Mon Jun 28 2010 Adam Jackson <ajax@redhat.com> 1.3-2
- libX11-1.3.1-creategc-man-page.patch: Fix man page for XCreateGC (#581583)

* Tue Oct 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3-1
- libX11 1.3

* Thu Aug 13 2009 Parag <paragn@fedoraproject.org> 1.2.99-5.20090805
- Merge-review cleanups #226062

* Thu Aug 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.99-4.20090805
- Today's git snapshot
- minor soname bump to 6.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.99-3.20090712
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.2.99-2.20090712
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Sun Jul 12 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.99-1.20090712
- Today's git snapshot
- libX11-1.2.1-indic.patch: Drop.

* Mon Jul 06 2009 Adam Jackson <ajax@redhat.com> 1.2.1-3
- -common subpackage

* Tue May 26 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.1-2
- libX11-1.2.1-indic.patch: Add new Indic language information to nls
  directory files (#497971)

* Tue May 26 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.1-1
- libX11 1.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Adam Jackson <ajax@redhat.com> 1.2-2
- Merge review cleanups. (#226062)

* Wed Feb 18 2009 Adam Jackson <ajax@redhat.com> 1.2-1
- libX11 1.2

* Wed Feb 04 2009 Adam Jackson <ajax@redhat.com> 1.1.99.2-4
- libX11-1.1.99.2-compose-updates.patch: Update compose sequences (from git)

* Mon Feb 02 2009 Caolán McNamara <caolanm@redhat.com> 1.1.99.2-3
- Resolves: rhbz#477174 don't hang in OOo, acroread, ekiga, xine, etc.

* Thu Dec 18 2008 Adam Jackson <ajax@redhat.com> 1.1.99.2-2
- BR: util-macros

* Thu Dec 18 2008 Adam Jackson <ajax@redhat.com> 1.1.99.2-1
- libX11 1.1.99.2

* Tue Nov 18 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.1.4-6
- libX11-1.1.4-XF86Suspend.patch: add XF86Suspend and XF86Hibernate keysyms.

* Fri Oct 24 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.1.4-5
- libX11-1.1.4-keysysm.patch: add a bunch of keysyms for remote controls and
  special keys.

* Wed Sep 17 2008 Adam Jackson <ajax@redhat.com> 1.1.4-4
- libX11-1.1.4-xcb-xreply-leak.patch: Fix the BadFont case.

* Wed Sep 17 2008 Adam Jackson <ajax@redhat.com> 1.1.4-3
- libX11-1.1.4-xcb-xreply-leak.patch: Fix a leak when the client has a
  non-fatal error handler. (mclasen, fdo #17616)

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.1.4-2
- Fix license tag.

* Thu Mar 06 2008 Adam Jackson <ajax@redhat.com> 1.1.4-1
- libX11 1.1.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.3-5
- Autorebuild for GCC 4.3

* Fri Oct 19 2007 Kristian Høgsberg <krh@redhat.com> - 1.1.3-4
- Add patch from upstream to add keysyms for brightness buttons (#330491).

* Tue Oct 16 2007 Adam Jackson <ajax@redhat.com> 1.1.3-3
- libX11-devel Requires: libxcb-devel.

* Wed Oct 10 2007 Adam Jackson <ajax@redhat.com> 1.1.3-2
- libX11-1.1.3-xkb-lock-fix.patch: Don't LockDisplay() recursively.  Fixes
  Gnome hang at logout. (#326461)

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.1.3-1
- libX11 1.1.3

* Thu Sep 20 2007 Adam Jackson <ajax@redhat.com> 1.1.2-4
- Update xtrans dep and rebuild.

* Mon Sep 17 2007 Adam Jackson <ajax@redhat.com> 1.1.2-3
- libX11-1.1.2-GetMotionEvents.patch: Fix the definition of XGetMotionEvents
  to match the argument order in the headers. (#274671)

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.1.2-2
- Rebuild for build id

* Mon Jul 23 2007 Adam Jackson <ajax@redhat.com> 1.1.2-1
- libX11 1.1.2.
- Enable XCB for libX11 transport.

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.3-9
- Don't install INSTALL

* Fri Apr 06 2007 Adam Jackson <ajax@redhat.com> 1.0.3-8
- Fix for CVE 2007-1667.

* Mon Jan 29 2007 Adam Jackson <ajax@redhat.com> 1.0.3-7
- Fix xim fd leak.

* Thu Nov 09 2006 Caius Chance <cchance@redhat.com> 1.0.3-6.fc7
- Fix XIM hangs when switching input context (Soren Sandmann, #201284)

* Fri Oct 13 2006 Kristian Høgsberg <krh@redhat.com> 1.0.3-5.fc7
- Add pkgconfig dependency for -devel package.

* Sat Sep 30 2006 Soren Sandmann <sandmann@redhat.com> 1.0.3-4.fc6
- Fix patch so it actually applies. (#208508)

* Sat Sep 30 2006 Soren Sandmann <sandmann@redhat.com> 1.0.3-4.fc6
- Fix typos in patch for indic locales (#208580)

* Wed Sep 20 2006 Soren Sandmann <sandmann@redhat.com> 1.0.3-3.fc6
- Add patch to not forward keycode 0 (#194357).

* Wed Jul 19 2006 Mike A. Harris <mharris@redhat.com> 1.0.3-2.fc6
- Added libX11-nls-indic-locales-bug185376.patch to add support for various
  indic locales which have now been committed upstream (#185376)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.3-1.1.fc6
- rebuild

* Mon Jul 10 2006 Mike A. Harris <mharris@redhat.com> 1.0.3-1.fc6
- Updated libX11 to version 1.0.3
- Remove libX11-1.0.1-setuid.diff as it is included in the 1.0.3 release.
- Added 'dist' tag to "Release:"

* Wed Jun 28 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-1
- Updated libX11 to version 1.0.2
- Bump BuildRequires and Requires to "xorg-x11-proto-devel >= 7.1-2" to meet
  new "xproto >= 7.0.6" dependency.
- Disable libX11-0.99.3-datadir-locale-dir-fix.patch as it is now included
  upstream.
- Remove autoconf dependency as we no longer need it.

* Tue Jun 20 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added libX11-1.0.1-setuid.diff to fix potential security issue (#196094)
- Change dependency on "filesystem" package to "xorg-x11-filesystem" package,
  so we can control this dep centrally.
- Added NEWS to doc list.

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Remove package ownership of mandir/libdir/etc.

* Fri May 12 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-1
- Bump to 1.0.1

* Thu Feb 23 2006 Christopher Aillon <caillon@redhat.com> 1.0.0-3
- Look for the versioned libXcursor.so.1 (fixes 179044)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Dec 24 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Added "Requires: libXau-devel, libXdmcp-devel" to -devel subpackage (#176313)

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libX11 to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.4-1
- Updated libX11 to version 0.99.4 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-4
- Added libX11-0.99.3-datadir-locale-dir-fix.patch, to fix build to install
  the locale data files into datadir instead of libdir. (#173282)

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.3-3
- require newer filesystem package (#172610)

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-2
- Moved _smp_mflags from 'make install' to 'make' invocation, duh.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libX11 to version 0.99.3 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Nov 07 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Fix devel subpackage summary and description with s/libXdmcp/libX11/

* Fri Oct 21 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to libX11-0.99.2 from the X11R7 RC1 release.
- Added en_GR.UTF-8 locale to file manifest.
- Forcibly remove Xcms.txt

* Sun Oct 02 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Added _smp_mflags to make invocation to speed up SMP builds

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1.1
- Added Requires: xorg-x11-proto-devel to libX11-devel subpackage

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
