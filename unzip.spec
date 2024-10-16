%global debug_package %{nil}
%define src_ver %(echo %{version}|sed "s/\\.//"g)

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		unzip
Version:	6.00
Release:	3
License:	BSD-like
Group:		Archiving/Compression
URL:		https://www.info-zip.org/pub/infozip/UnZip.html
# Some newer beta versions (up to 610c25) can be found at
# http://antinode.info/ftp/info-zip/ - but since the project seems
# to have been abandoned upstream for more than a decade, it's
# unlikely we'll ever see a release based on those.
# Better to stick with an (albeit abandoned as well) release that
# at least gets fixes from other distros...
Source0:	http://downloads.sourceforge.net/infozip/unzip60.tar.gz
# From Fedora
Patch100:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-bzip2-configure.patch
Patch101:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-exec-shield.patch
Patch102:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-close.patch
Patch103:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-attribs-overflow.patch
Patch104:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-configure.patch
Patch105:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-manpage-fix.patch
Patch106:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-fix-recmatch.patch
Patch107:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-symlink.patch
Patch108:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-caseinsensitive.patch
Patch109:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-format-secure.patch
Patch110:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-valgrind.patch
Patch111:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-x-option.patch
Patch112:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-overflow.patch
Patch113:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2014-8139.patch
Patch114:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2014-8140.patch
Patch115:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2014-8141.patch
Patch116:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-overflow-long-fsize.patch
Patch117:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-heap-overflow-infloop.patch
Patch118:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-alt-iconv-utf8.patch
Patch119:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-alt-iconv-utf8-print.patch
Patch120:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/0001-Fix-CVE-2016-9844-rhbz-1404283.patch
Patch121:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-timestamp.patch
Patch122:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2018-1000035-heap-based-overflow.patch
Patch123:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-cve-2018-18384.patch
Patch124:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-COVSCAN-fix-unterminated-string.patch
Patch125:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part1.patch
Patch126:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part2.patch
Patch127:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part3.patch
Patch128:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-manpage.patch
Patch129:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part4.patch
Patch130:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part5.patch
Patch131:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-part6.patch
Patch132:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-zipbomb-switch.patch
Patch133:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-gnu89-build.patch
Patch134:	https://src.fedoraproject.org/rpms/unzip/raw/rawhide/f/unzip-6.0-wcstombs-fortify.patch
# From Mark Adler's fork
Patch200:	https://github.com/madler/unzip/commit/d685e65d71339cbdc0926b4cce072b6c15bb9b74.patch
Patch201:	https://github.com/madler/unzip/commit/9e1f83500aa502fdc3a42ad0bd560bf7c1909298.patch
Patch202:	https://github.com/madler/unzip/commit/1860ba704db791db940475b1fb6ef73bdb81bcab.patch
Patch203:	https://github.com/madler/unzip/commit/0b82c20ac7375b522215b567174f370be89a4b12.patch
# OpenMandriva specific
Patch300:	unzip-6.0-unicode-buildfix.patch
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
sed -i -e 's,CC=gcc,CC="%{__cc}",g;s,LD=gcc,LD="%{__cc}",g' unix/Makefile
%make_build -j1 -f unix/Makefile linux_noasm CF="%{optflags} -I. -DNO_LCHMOD -DUNIX -DIZ_HAVE_UXUIDGID -DZIP64_SUPPORT -DLARGE_FILE_SUPPORT -DUNICODE_SUPPORT -DUTF8_MAYBE_NATIVE -D_MBCS" LFLAGS1="%{build_ldflags}" LFLAGS2="%{build_ldflags}"

%if ! %{cross_compiling}
%check
make test -f unix/Makefile
%endif

%install
make -f unix/Makefile prefix=%{buildroot}%{_prefix} MANDIR=%{buildroot}%{_mandir}/man1 INSTALL="cp -p" install

%files
%doc BUGS COPYING.OLD Contents History.* README ToDo
%doc proginfo/
%{_bindir}/*
%doc %{_mandir}/man1/*
