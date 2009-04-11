%define name	unzip
%define version 5.52
%define release %mkrel 7
%define src_ver	%(echo %version|sed "s/\\.//"g)

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://ftp.info-zip.org/pub/infozip/src/%{name}%{src_ver}.tar.bz2
Patch1:		unzip552-size-64bit.patch
Patch2:		unzip-5.52-CAN-2005-2475.patch
Patch3:		unzip-5.52-CVE-2005-4667.patch
Patch4:		unzip-5.52-CVE-2008-0888.diff
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
License:	BSD-like
Group:		Archiving/Compression
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%prep

%setup -q
%patch1 -p0 -b .64bit
%patch2 -p1 -b .can-2005-2475
%patch3 -p1 -b .cve-2005-4667
%patch4 -p0 -b .CVE-2008-0888

%build
%ifarch %{ix86}
#gw FIXME: do we still need to disable LZW?
%define Werror_cflags %nil
%make -ef unix/Makefile linux CF="-DLZW_CLEAN %{optflags} -D_FILE_OFFSET_BITS=64 -Wall -I. -DASM_CRC" CC=gcc LD=gcc AS=gcc AF="-Di386" CRC32=crc_gcc
%else
%make -ef unix/Makefile linux_noasm CF="-DLZW_CLEAN %{optflags} -D_FILE_OFFSET_BITS=64 -Wall -I."
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

ln -sf unzip zipinfo
for i in unzip funzip unzipsfx zipinfo;	do install $i %{buildroot}%{_bindir}; done
install unix/zipgrep %{buildroot}%{_bindir}

for i in man/*.1; do install -m 644 $i %{buildroot}%{_mandir}/man1/; done

cat > README.IMPORTANT.Mandriva << EOF
This version of unzip is a stripped-down version which doesn't include
the "unreduce" and "unshrink" algorithms. The first one is subject to
a restrictive copyright by Samuel H. Smith which forbids its use in
commercial products; and Unisys claimed a patent ("Welsh patent") on the 
second one (while their licensing would seem to mean that an
extractor-only program would not be covered).

Since the rest of the code is copyrighted by Info-Zip under a BSD-like
license, this Mandriva package is covered by this license.

Please note that currently, default compilation of the Info-Zip
distribution also excludes the unreduce and unshrink code.

Please contact Mandriva at <bugs@mandriva.com> if you have
any problems regarding this issue.
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS COPYING.OLD Contents History.* INSTALL README ToDo WHERE README.IMPORTANT.Mandriva
%doc proginfo/
%{_bindir}/*
%{_mandir}/man1/*


