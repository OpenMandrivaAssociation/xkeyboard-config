%define old_name x11-data-xkbdata

%define git_url git://anongit.freedesktop.org/xkeyboard-config

Name: xkeyboard-config
Epoch: 1
Version: 2.1
Release: %mkrel 2
BuildArch: noarch
Summary: XKB data files
URL:   http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Group: Development/X11
Source: xkeyboard-config-%{version}.tar.bz2

# symbols/kg and symbols/la besides looking very simple patches, did not apply
#   cleanly, so removed for now
# Dropped all conflicting patches
# (cg) When doing 1.3->1.4 rediff the tj keymap changes were dropped
# due to an upstream change that seems to address the issue differently
Patch0: xkeyboard-config-1.4-fixkbd.patch

# (Anssi 09/2008) Add fi(kotoistus_classic_nbsp) and use that by default.
# It has nbsp in level4 instead of level3 to avoid typos, as in fi(classic).
# See http://bugs.freedesktop.org/show_bug.cgi?id=12764
# Comments have been sent to the Kotoistus project.
Patch1: xkeyboard-config-1.9-fi-kotoistus_classic_nbsp.patch

# Morocco symbols/tifinagh should be symbols/ma in the official version
# Nigerian symbols/ng seens to match
# Pakistanese is pk in 1.1, not snd
# symbols/tm "Turkmen" is the same as symbols/tr "Turkey" in 1.1? seens
#	quite different
# symbols/urd seens to be 1.1's symbols/in (claims support for all Indian
#	keyboard layouts)
# symbols/kur "Kurdish" is apparently in several different Kurdish support
#	files/descriptions
# symbols/chr "Cherokee" being dropped? or already integrated in some other
#	description?
Patch2: xkbdata-1.0.1-newkbd.patch

# Keeping for bugzilla #28919
Patch4: xkb-fix_uz.patch
# (fc) 1.5-2mdv map key_battery, wlan, bluetooth, uwb to their XF86 keycodes (GIT)
Patch6: xkeyboard-config-1.4-battery.patch
# Revert change that disables zapping by default
Patch9: xkeyboard-config-1.9-Enable-zapping-by-default.patch

License: MIT
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: xkbcomp >= 1.0.1
BuildRequires: perl-XML-Parser
BuildRequires: intltool
BuildRequires: glib-gettextize
# https://qa.mandriva.com/show_bug.cgi?id=44052
BuildRequires: gettext-devel

%description
Xkeyboard-config provides consistent, well-structured, frequently released of X
keyboard configuration data (XKB) for various X Window System implementations.

%package -n %{old_name}
Summary: %{summary}
Group: %{group}

%description -n %{old_name}
Xkeyboard-config provides consistent, well-structured, frequently released of X
keyboard configuration data (XKB) for various X Window System implementations.

%prep
%setup -q 

# Keyboard fixes patches -- pablo
%patch0 -p1 -b .fixkbd

	#   Not applied as most are already implemented, but in a compeletely
	#   different way. May need some review as described for Patch2:
	#   Still just keeping the old patch for reference in case problems
	#   arise.
# New keyboard layouts -- pablo
# %patch2 -p1 -b .newkbd
# needed by patch2
# automake

%patch1 -p1
%patch4 -p1 -b .uz_fix
%patch6 -p1 -b .battery
%patch9 -p1 -b .enable-zapping

# fix build
aclocal
autoconf

%build
%configure2_5x --enable-compat-rules \
    		--with-xkb-base=%{_datadir}/X11/xkb \
    		--disable-xkbcomp-symlink \
    		--with-xkb-rules-symlink=xorg

%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_localstatedir}/lib/xkb
#need this symlink for xkb to work (Mdv bug #34195)
ln -snf %{_localstatedir}/lib/xkb $RPM_BUILD_ROOT/usr/share/X11/xkb/compiled

%find_lang %{name}

%clean
rm -rf %{buildroot}

%pre -n %{old_name}
# this was a directory in the old installation
if [ -d "%{_datadir}/X11/xkb/compiled" ]; then
	rm -rf %{_datadir}/X11/xkb/compiled
fi

%files -f %{name}.lang -n %{old_name}
%defattr(-,root,root)
%dir %{_datadir}/X11/xkb/
%attr(1777,root,root) %dir %{_localstatedir}/lib/xkb
%{_datadir}/X11/xkb/*
%{_datadir}/pkgconfig/xkeyboard-config.pc
