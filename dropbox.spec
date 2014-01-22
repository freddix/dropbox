Summary:	Sync and backup files between computers
Name:		dropbox
Version:	2.6.2
Release:	4
License:	Proprietary
Group:		Daemons
URL:		http://www.dropbox.com/
Source0:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86-%{version}.tar.gz
# Source0-md5:	06f0370e55e700f7c78f206101550a4b
Source1:	http://dl-web.dropbox.com/u/17/%{name}-lnx.x86_64-%{version}.tar.gz
# Source1-md5:	130e6f895309d953a7d884538fc97746
BuildRequires:	tar
BuildRequires:	unzip
BuildRequires:	zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# generate no Provides from private modules
%define		_noautoprovfiles	%{_libdir}/%{name}

# provided by package itself, but autodeps disabled
%define		_noautoreq		libcrypto.so libssl.so libwx_.*.so librsync.so.1

# a zip and executable at the same time
%define		_noautostrip	.*/library.zip\\|.*/dropbox

# debuginfo wouldn't be useful
%define		_enable_debug_packages	0

# prelinked library, it is missing some cairo symbols
%define		skip_post_check_so	libwx_gtk2ud_core-2.8.so.0

%description
Dropbox is software that syncs your files online and across your
computers.

Put your files into your Dropbox on one computer, and they'll be
instantly available on any of your other computers that you've
installed Dropbox on (Windows, Mac, and Linux too!) Because a copy of
your files are stored on Dropbox's secure servers, you can also access
them from any computer or mobile device using the Dropbox website.

%prep
%setup -qcT
%ifarch %{ix86}
%{__tar} --strip-components=1 -xzf %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} --strip-components=1 -xzf %{SOURCE1}
%endif

# libraries to be taken from system
# for a in *.so*; do ls -ld /lib/$a /usr/lib/$a; done 2>/dev/null
%{__rm} libpng12.so.0 libbz2.so.1.0 libpopt.so.0 libffi.so.6

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
ln -sf dropbox library.zip

# fun, let's delete non-linux files from archive
unzip -l library.zip | grep -E 'arch/(mac|win32)|pynt|ui/cocoa|unittest' | awk '{print $NF}' > lib.delete
# TODO: also pymac could be cleaned if pymac.constants is not imported
zip library.zip -d $(cat lib.delete)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
ln -s %{_libdir}/%{name}/dropboxd $RPM_BUILD_ROOT%{_bindir}/dropboxd

# install everything else
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a . $RPM_BUILD_ROOT%{_libdir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/lib.delete

# in doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/{ACKNOWLEDGEMENTS,VERSION,README}

# win binaries
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/distribute-*.egg/setuptools/*.exe

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS VERSION README
%attr(755,root,root) %{_bindir}/dropboxd
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%attr(755,root,root) %{_libdir}/%{name}/dropbox
%attr(755,root,root) %{_libdir}/%{name}/dropboxd
%{_libdir}/%{name}/*.egg-info
%{_libdir}/%{name}/library.zip

%dir %{_libdir}/%{name}/images
%{_libdir}/%{name}/images/emblems
%{_libdir}/%{name}/images/hicolor

%dir %{_libdir}/%{name}/cffi-*.egg
%attr(755,root,root) %{_libdir}/%{name}/cffi-*.egg/*.so
%{_libdir}/%{name}/cffi-*.egg/*.py[co]
%{_libdir}/%{name}/cffi-*.egg/EGG-INFO
%dir %{_libdir}/%{name}/cffi-*.egg/cffi
%{_libdir}/%{name}/cffi-*.egg/cffi/*.py[co]

%dir %{_libdir}/%{name}/distribute-*.egg
%{_libdir}/%{name}/distribute-*.egg/*.py[co]
%dir %{_libdir}/%{name}/distribute-*.egg/setuptools
%{_libdir}/%{name}/distribute-*.egg/setuptools/*.py[co]
%dir %{_libdir}/%{name}/distribute-*.egg/setuptools/command
%{_libdir}/%{name}/distribute-*.egg/setuptools/command/*.py[co]
%dir %{_libdir}/%{name}/distribute-*.egg/setuptools/tests
%{_libdir}/%{name}/distribute-*.egg/setuptools/tests/*.py[co]
%{_libdir}/%{name}/distribute-*.egg/EGG-INFO

%dir %{_libdir}/%{name}/dropbox_sqlite_ext-*.egg
%dir %{_libdir}/%{name}/dropbox_sqlite_ext-*.egg/dropbox_sqlite_ext
%attr(755,root,root) %{_libdir}/%{name}/dropbox_sqlite_ext-*.egg/dropbox_sqlite_ext/*.so
%{_libdir}/%{name}/dropbox_sqlite_ext-*.egg/dropbox_sqlite_ext/*.py[co]
%{_libdir}/%{name}/dropbox_sqlite_ext-*.egg/EGG-INFO

%dir %{_libdir}/%{name}/mock-*.egg
%{_libdir}/%{name}/mock-*.egg/mock.py[co]
%{_libdir}/%{name}/mock-*.egg/EGG-INFO

