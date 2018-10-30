%define src_ver	%(echo %{version}|sed "s/\\.//"g)

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		unzip
Version:	6.0
Release:	26
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
#Source0:	http://ftp.info-zip.org/pub/infozip/src/%{name}%{src_ver}.tar.bz2
Source0:	http://antinode.info/ftp/info-zip/unzip610c23.zip
BuildRequires:  pkgconfig(zlib)

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%prep
%setup -qn %{name}610c23
%autopatch -p1

%build
%define Werror_cflags %nil
%global optflags %optflags -O3
%setup_compile_flags
sed -i -e 's,CC=gcc,CC=%{__cc},g;s,LD=gcc,LD=%{__cc},g' unix/Makefile
%make_build -j1 -f unix/Makefile linux_noasm CF="%{optflags} -I. -DNO_LCHMOD" LF1="%{optflags}"

%check
make test -f unix/Makefile

%install
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

ln -sf unzip zipinfo
for i in unzip funzip unzipsfx zipinfo;	do install $i %{buildroot}%{_bindir}; done
install unix/zipgrep %{buildroot}%{_bindir}

for i in man/man1/*.1; do install -m 644 $i %{buildroot}%{_mandir}/man1/; done

cat > README.IMPORTANT.OpenMandriva << EOF
This version of unzip include the "unreduce" and "unshrink" algorithms.
Since 20 June 2003 LZW patents has expired !


Please contact OpenMandriva at <http://issues.openmandriva.org> if you have
any problems regarding this issue.
EOF

%files
%doc BUGS COPYING.OLD Contents History.* README ToDo README.IMPORTANT.OpenMandriva
%doc proginfo/
%{_bindir}/*
%{_mandir}/man1/*
