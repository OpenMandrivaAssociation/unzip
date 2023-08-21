%global debug_package %{nil}
%define src_ver %(echo %{version}|sed "s/\\.//"g)

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		unzip
Version:	6.00
Release:	2
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
# Some newer beta versions (up to 610c25) can be found at
# http://antinode.info/ftp/info-zip/ - but since the project seems
# to have been abandoned upstream for more than a decade, it's
# unlikely we'll ever see a release based on those.
# Better to stick with an (albeit abandoned as well) release that
# at least gets fixes from other distros...
Source0:	http://downloads.sourceforge.net/infozip/unzip60.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-bzip2-configure.patch
Patch1:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-exec-shield.patch
Patch2:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-close.patch
Patch3:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-attribs-overflow.patch
Patch4:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-configure.patch
Patch5:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-manpage-fix.patch
Patch6:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-fix-recmatch.patch
Patch7:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-symlink.patch
Patch8:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-caseinsensitive.patch
Patch9:		https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-format-secure.patch
Patch10:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-valgrind.patch
Patch11:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-x-option.patch
Patch12:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-overflow.patch
Patch13:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2014-8139.patch
Patch14:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2014-8140.patch
Patch15:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2014-8141.patch
Patch16:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-overflow-long-fsize.patch
Patch17:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-heap-overflow-infloop.patch
Patch18:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-alt-iconv-utf8.patch
Patch19:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-alt-iconv-utf8-print.patch
Patch20:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/0001-Fix-CVE-2016-9844-rhbz-1404283.patch
Patch21:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-timestamp.patch
Patch22:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2018-1000035-heap-based-overflow.patch
Patch23:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2018-18384.patch
Patch24:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-COVSCAN-fix-unterminated-string.patch
Patch25:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part1.patch
Patch26:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part2.patch
Patch27:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part3.patch
Patch28:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-manpage.patch
Patch29:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part4.patch
Patch30:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part5.patch
Patch31:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part6.patch
Patch32:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-switch.patch
Patch33:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-gnu89-build.patch
Patch34:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-wcstombs-fortify.patch
BuildRequires:	pkgconfig(zlib)

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%prep
%autosetup -n %{name}60 -p1

%build
%define Werror_cflags %nil
%global optflags %optflags -O3
%set_build_flags
sed -i -e 's,CC=gcc,CC=%{__cc},g;s,LD=gcc,LD=%{__cc},g' unix/Makefile
%make_build -j1 -f unix/Makefile linux_noasm CF="%{optflags} -I. -DNO_LCHMOD -DUNIX -DIZ_HAVE_UXUIDGID" LFLAGS1="%{build_ldflags}" LFLAGS2="%{build_ldflags}"

%check
make test -f unix/Makefile

%install
make -f unix/Makefile prefix=%{buildroot}%{_prefix} MANDIR=%{buildroot}%{_mandir}/man1 INSTALL="cp -p" install

%files
%doc BUGS COPYING.OLD Contents History.* README ToDo
%doc proginfo/
%{_bindir}/*
%doc %{_mandir}/man1/*
