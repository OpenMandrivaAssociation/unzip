%define src_ver	%(echo %{version}|sed "s/\\.//"g)

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		unzip
Version:	6.0
Release:	21
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:	http://ftp.info-zip.org/pub/infozip/src/%{name}%{src_ver}.tar.bz2
Patch0:		%{name}-6.0-libnatspec.patch
# Not sent to upstream.
Patch1:		unzip-6.0-bzip2-configure.patch
# Upstream plans to do this in zip (hopefully also in unzip).
Patch2:		unzip-6.0-exec-shield.patch
# Upstream plans to do similar thing.
Patch3:		unzip-6.0-close.patch
# Details in rhbz#532380.
# Reported to upstream: http://www.info-zip.org/board/board.pl?m-1259575993/
Patch4:		unzip-6.0-attribs-overflow.patch
# Not sent to upstream, as it's Fedora/RHEL specific.
# Modify the configure script not to request the strip of binaries.
Patch5:		unzip-6.0-nostrip.patch
Patch6:		unzip-6.0-manpage-fix.patch
# Update match.c with recmatch() from zip 3.0's util.c
# This also resolves the license issue in that old function.
# Original came from here: https://projects.parabolagnulinux.org/abslibre.git/plain/libre/unzip-libre/match.patch
Patch7:		unzip-6.0-fix-recmatch.patch
# Update process.c
Patch8:		unzip-6.0-symlink.patch
# change using of macro "case_map" by "to_up"
Patch9:		unzip-6.0-caseinsensitive.patch
# downstream fix for "-Werror=format-security"
# upstream doesn't want hear about this option again
Patch10:	unzip-6.0-format-secure.patch
Patch11:	unzip-6.0-valgrind.patch
Patch12:	unzip-6.0-x-option.patch
Patch13:	unzip-6.0-overflow.patch
Patch14:	unzip-6.0-cve-2014-8139.patch
Patch15:	unzip-6.0-cve-2014-8140.patch
Patch16:	unzip-6.0-cve-2014-8141.patch
Patch17:	unzip-6.0-overflow-long-fsize.patch
# Fix heap overflow and infinite loop when invalid input is given (#1260947)
Patch18:	unzip-6.0-heap-overflow-infloop.patch
# from debian
Patch19:	19-cve-2016-9844-zipinfo-buffer-overflow.patch
Patch20:	01-manpages-in-section-1-not-in-section-1l.patch
Patch21:	04-handle-pkware-verification-bit.patch
Patch22:	08-allow-greater-hostver-values.patch
Patch23:	13-remove-build-date.patch
Patch24:	17-restore-unix-timestamps-accurately.patch


BuildRequires:	libnatspec-devel
BuildRequires:	bzip2-devel

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%prep

%setup -qn %{name}%{src_ver}
%apply_patches

%build
# remove gcc and weird cflags\ldflags
sed -i \
        -e '/^CFLAGS/d' \
        -e '/CFLAGS/s:-O[0-9]\?:$(CFLAGS) $(CPPFLAGS):' \
        -e '/^STRIP/s:=.*:=true:' \
        -e "s:\<CC=gcc\>:CC=\"%{__cc}\":" \
        -e "s:\<LD=gcc\>:LD=\"%{__cc}\":" \
        -e "s:\<AS=gcc\>:AS=\"%{__cc}\":" \
        -e 's:LF2 = -s:LF2 = :' \
        -e 's:LF = :LF = $(LDFLAGS) :' \
        -e 's:SL = :SL = $(LDFLAGS) :' \
        -e 's:FL = :FL = $(LDFLAGS) :' \
        -e 's:$(AS) :$(AS) $(ASFLAGS) :g' \
        unix/Makefile
# flags
# Delete bundled code to make sure we don't use it.
rm -r bzip2

COMMFLAGS="-DNOMEMCPY -DIZ_HAVE_UXUIDGID -D_FILE_OFFSET_BITS=64 -DACORN_FTYPE_NFS -DWILD_STOP_AT_DIR -DLARGE_FILE_SUPPORT -DUNICODE_SUPPORT -DUNICODE_WCHAR -DUTF8_MAYBE_NATIVE -DNO_LCHMOD -DDATE_FORMAT=DF_YMD -DNATIVE -Wall -I."
IX86FLAGS="-DNOMEMCPY -DIZ_HAVE_UXUIDGID -D_FILE_OFFSET_BITS=64 -DACORN_FTYPE_NFS -DWILD_STOP_AT_DIR -DLARGE_FILE_SUPPORT -DUNICODE_SUPPORT -DUNICODE_WCHAR -DUTF8_MAYBE_NATIVE -DNO_LCHMOD -DDATE_FORMAT=DF_YMD -DNATIVE -Wall -I. -DASM_CRC"

%ifarch %{ix86}
%make -ef unix/Makefile linux CF="%{optflags} $IX86FLAGS" CC=%{__cc} LF2="%{ldflags} -lnatspec" LD=%{__cc} AS=%{__cc} AF="-Di386" CRC32=crc_gcc
%else
%make -ef unix/Makefile linux_noasm CC=%{__cc} LF2="%{ldflags} -lnatspec" LD=%{__cc} CF="%{optflags} $COMMFLAGS"
%endif

%check
make test -f unix/Makefile

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
