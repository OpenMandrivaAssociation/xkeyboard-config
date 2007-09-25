%define pkgversion 0.8
Name: x11-data-xkbdata
Epoch: 1
Version: %{pkgversion}
Release: %mkrel 4
BuildArch: noarch
Summary: Alternative xkb data files
URL:   http://www.freedesktop.org/wiki/Software_2fXKeyboardConfig
Group: Development/X11
Source: http://xlibs.freedesktop.org/xkbdesc/xkeyboard-config-%{pkgversion}.tar.bz2 
Source1: xkbd_new_names.pl
Patch0: xkbdata-1.0.1-fixkbd.patch
Patch1: xkbdata-1.0.1-remove_duplicated.patch
Patch2: xkbdata-1.0.1-newkbd.patch
# for compatibility
Patch3: xkbdata-1.0.1-oldkbd.patch
Patch4: xkb-fix_uz.patch
Patch5: xkb-logitech_volumekey_fix.patch
Patch6: xkb-logiink_fix.patch

License: MIT
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: xkbcomp >= 1.0.1
BuildRequires: perl-XML-Parser

%description
Xkeyboard-config provides consistent, well-structured, frequently released of X
keyboard configuration data (XKB) for various X Window System implementations.

%prep
%setup -q -n xkeyboard-config-%{pkgversion}
# Keyboard fixes patches -- pablo
%patch0 -p1 -b .fixkbd
# remove duplicate keyboards from the list
%patch1 -p1 -b .remdup
# New keyboard layouts -- pablo
%patch2 -p1 -b .newkbd
# Some old keyboard names, for compatibility (to remove for 2008) -- pablo
%patch3 -p1 -b .oldkbd
%patch4 -p1 -b .uz_fix
%patch5 -p1 -b .logitech_volume
%patch6 -p1 -b .logiink

%build
%configure2_5x	--x-includes=%{_includedir}\
		--x-libraries=%{_libdir} \
		--enable-compat-rules \
    		--with-xkb-base=%{_datadir}/X11/xkb \
    		--disable-xkbcomp-symlink \
    		--with-xkb-rules-symlink=xorg

%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_localstatedir}/xkb

%clean
rm -rf %{buildroot}

%pre
# this was a directory in the old installation
if [ -d "%{_datadir}/X11/xkb/compiled" ]; then
	rm -rf %{_datadir}/X11/xkb/compiled
fi

%files
%defattr(-,root,root)
%dir %{_datadir}/X11/xkb/
%dir %{_localstatedir}/xkb
%{_datadir}/X11/xkb/*


