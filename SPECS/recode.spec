Summary: Conversion between character sets and surfaces
Name: recode
Version: 3.6
Release: 47%{?dist}
License: GPLv2+
Group: Applications/File
Url:    http://recode.progiciels-bpi.ca/
Source: http://recode.progiciels-bpi.ca/archives/recode-%{version}.tar.gz
Patch0: recode.patch
Patch1: recode-3.6-getcwd.patch
Patch2: recode-bool-bitfield.patch
Patch3: recode-flex-m4.patch
Patch4: recode-automake.patch
Patch5: recode-format-security.patch
Patch6: recode-longfilename.patch

Requires(post): /sbin/install-info
Requires(post): /sbin/ldconfig
Requires(preun): /sbin/install-info
Requires(postun): /sbin/ldconfig

BuildRequires: libtool
BuildRequires: texinfo


%description
The `recode' converts files between character sets and usages.
It recognizes or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations.  Most RFC 1345 character sets
are supported.

%package devel
Summary: Header files for development using recode
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The `recode' library converts files between character sets and usages.
The library recognizes or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations. Most RFC 1345 character sets
are supported.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .getcwd
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
rm m4/libtool.m4
rm acinclude.m4

%build
autoreconf -fiv
%configure --disable-static
make %{?_smp_mflags}

%check
make check

%install
%makeinstall
%find_lang %{name}

# remove unpackaged file from the buildroot
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# remove libtool archives
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/recode.info.gz %{_infodir}/dir --entry="* recode: (recode).                        Conversion between character sets and surfaces." || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/recode.info.gz %{_infodir}/dir --entry="* recode: (recode).                        Conversion between character sets and surfaces." || :
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING* ChangeLog NEWS README THANKS TODO
%{_mandir}/*/*
%{_infodir}/recode.info*
%{_bindir}/*
%{_libdir}/*.so.0*

%files devel
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6-47
- Escape macros in %%changelog

* Tue Oct 03 2017 Zoltan Kota <zoltank[AT]gmail.com> - 3.6-46
- Apply patch to fix bug #1422550

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 18 2013 Jiri Popelka <jpopelka@redhat.com> - 3.6-38
- Fix FTBFS if "-Werror=format-security" flag is used (#1037305).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Zoltan Kota <zoltank[AT]gmail.com> 3.6-36
- Fix failed Fedora_19_Mass_Rebuild [bug #914431].

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-34
- Add patch for fixing build with new automake.
  (Fixes failed Fedora_18_Mass_Rebuild.)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Zoltan Kota <zoltank[AT]gmail.com> 3.6-32
- Corrected summary of the devel subpackage. Fixing bug #817947.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 7 2010 Zoltan Kota <z.kota[AT]gmx.net> 3.6-29
- Fix build on x86_64. Run autoreconf to update config files.
  autoconf >= 2.64 needs to patch the flex.m4 file.
  Fixing FTBFS bug #564601.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6-26
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Zoltan Kota <z.kota[AT]gmx.net> 3.6-25
- add patch for gcc43

* Wed Aug 22 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-24
- update license tag
- rebuild

* Tue Apr 03 2007 Zoltan Kota <z.kota[AT]gmx.net> 3.6-23
- rebuild

* Fri Sep 01 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-22
- rebuild

* Mon Feb 13 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-21
- rebuild

* Thu Dec 22 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-20
- rebuild

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-19
- fix requires
- disable static libs and remove libtool archives
- add %%doc

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-18
- add dist tag
- specfile cleanup

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 3.6-17
- rebuild for Extras

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.6-16
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.6-15
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 3.6-14
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Than Ngo <than@redhat.com> 3.6-11 
- add a patch file from kota@szbk.u-szeged.hu (bug #115524)

* Thu Nov 20 2003 Thomas Woerner <twoerner@redhat.com> 3.6-10
- Fixed RPATH (missing make in %%build)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 3.6-7
- rebuild on all arches
- remove unpackaged file from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 15 2002 Bill Nottingham <notting@redhat.com> 3.6-4
- add ldconfig %%post/%%postun

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 3.6-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 13 2001 Than Ngo <than@redhat.com> 3.6-1
- initial RPM for 8.0
