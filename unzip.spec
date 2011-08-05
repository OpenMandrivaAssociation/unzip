%define name	unzip
%define version 6.0
%define release %mkrel 6
%define src_ver	%(echo %version|sed "s/\\.//"g)

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:	http://ftp.info-zip.org/pub/infozip/src/%{name}%{src_ver}.tar.bz2
Patch0:		%{name}-6.0-libnatspec.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
%make -ef unix/Makefile linux_noasm CF="%{optflags} -D_FILE_OFFSET_BITS=64 -DACORN_FTYPE_NFS -DWILD_STOP_AT_DIR -DLARGE_FILE_SUPPORT -DUNICODE_SUPPORT -DUNICODE_WCHAR -DUTF8_MAYBE_NATIVE -DNO_LCHMOD -DDATE_FORMAT=DF_YMD -DNATIVE -Wall -I."
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

ln -sf unzip zipinfo
for i in unzip funzip unzipsfx zipinfo;	do install $i %{buildroot}%{_bindir}; done
install unix/zipgrep %{buildroot}%{_bindir}

for i in man/*.1; do install -m 644 $i %{buildroot}%{_mandir}/man1/; done

cat > README.IMPORTANT.Mandriva << EOF
This version of unzip include the "unreduce" and "unshrink" algorithms.
Since 20 June 2003 LZW patents has expired !


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
