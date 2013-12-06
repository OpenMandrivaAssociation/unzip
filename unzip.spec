%define src_ver	%(echo %{version}|sed "s/\\.//"g)

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		unzip
Version:	6.0
Release:	11
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:	http://ftp.info-zip.org/pub/infozip/src/%{name}%{src_ver}.tar.bz2
Patch0:		%{name}-6.0-libnatspec.patch
BuildRequires:	libnatspec-devel

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%prep

%setup -qn %{name}%{src_ver}
%patch0 -p1

%build
%define Werror_cflags %nil
%ifarch %{ix86}
%make -ef unix/Makefile linux CF="%{optflags} -D_FILE_OFFSET_BITS=64 -DACORN_FTYPE_NFS -DWILD_STOP_AT_DIR -DLARGE_FILE_SUPPORT -DUNICODE_SUPPORT -DUNICODE_WCHAR -DUTF8_MAYBE_NATIVE -DNO_LCHMOD -DDATE_FORMAT=DF_YMD -DNATIVE -Wall -I. -DASM_CRC" CC=gcc LD=gcc AS=gcc AF="-Di386" CRC32=crc_gcc
%else
%make -ef unix/Makefile linux_noasm CC=%{__cc} LD=%{__cc} CF="%{optflags} -D_FILE_OFFSET_BITS=64 -DACORN_FTYPE_NFS -DWILD_STOP_AT_DIR -DLARGE_FILE_SUPPORT -DUNICODE_SUPPORT -DUNICODE_WCHAR -DUTF8_MAYBE_NATIVE -DNO_LCHMOD -DDATE_FORMAT=DF_YMD -DNATIVE -Wall -I."
%endif

%install
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

ln -sf unzip zipinfo
for i in unzip funzip unzipsfx zipinfo;	do install $i %{buildroot}%{_bindir}; done
install unix/zipgrep %{buildroot}%{_bindir}

for i in man/*.1; do install -m 644 $i %{buildroot}%{_mandir}/man1/; done

cat > README.IMPORTANT.OpenMandriva << EOF
This version of unzip include the "unreduce" and "unshrink" algorithms.
Since 20 June 2003 LZW patents has expired !


Please contact OpenMandriva at <http://issues.openmandriva.org> if you have
any problems regarding this issue.
EOF

%files
%doc BUGS COPYING.OLD Contents History.* INSTALL README ToDo WHERE README.IMPORTANT.OpenMandriva
%doc proginfo/
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Fri Aug 05 2011 Andrey Bondrov <abondrov@mandriva.org> 6.0-6mdv2011.0
+ Revision: 693305
- Fix make flags for better non-latin locales support

* Wed Jul 06 2011 ÐÐ»ÐµÐºÑÐ°Ð½Ð´Ñ€ ÐšÐ°Ð·Ð°Ð½Ñ†ÐµÐ² <kazancas@mandriva.org> 6.0-5
+ Revision: 689029
- add patch for fix non-latin filenames in zip arch

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 6.0-4
+ Revision: 670747
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 6.0-3mdv2011.0
+ Revision: 608114
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 6.0-2mdv2010.1
+ Revision: 519078
- rebuild

* Mon Jul 27 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 6.0-1mdv2010.0
+ Revision: 401038
- update to new version 6.0
- enable LZW compression methods, since 2003 the patents are expired
- drop all patches
- spec file clean

* Sat Apr 11 2009 Funda Wang <fwang@mandriva.org> 5.52-8mdv2009.1
+ Revision: 366432
- disable formatchecking under all archs
- disable format checking
- reidff 64 bit patch

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 5.52-6mdv2009.0
+ Revision: 225903
- rebuild

* Tue Mar 18 2008 Oden Eriksson <oeriksson@mandriva.com> 5.52-5mdv2008.1
+ Revision: 188613
- fix #39030 (CVE-2008-0888: unzip - DoS and/or arbitrary code execution due to NEEDBITS macro)

* Mon Feb 25 2008 Olivier Blin <blino@mandriva.org> 5.52-4mdv2008.1
+ Revision: 174813
- build with _FILE_OFFSET_BITS=64 (#37178)
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 16 2007 Thierry Vignaud <tv@mandriva.org> 5.52-3mdv2008.0
+ Revision: 87711
- kill changelog left by repsys


* Tue Jan 30 2007 GÃ¶tz Waschk <waschk@mandriva.org> 5.52-2mdv2007.0
+ Revision: 115447
- Import unzip

* Tue Jan 30 2007 Götz Waschk <waschk@mandriva.org> 5.52-2mdv2007.1
- unpack patches

* Thu Mar 16 2006 Olivier Blin <oblin@mandriva.com> 5.52-2mdk
- from Stew Benedict: security update for CAN-2005-2475 (P2)
- from Vincent Danen: security fix for CVE-2005-4667 (P3)

* Thu May 05 2005 Götz Waschk <waschk@mandriva.org> 5.52-1mdk
- drop patch 0 and define LZW_CLEAN instead
- better source URL
- New release 5.52

* Mon May 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.51-1mdk
- fixes multiple vulnerabilities

