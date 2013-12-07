%define old_name x11-data-xkbdata

%define git_url git://anongit.freedesktop.org/xkeyboard-config

Name:		xkeyboard-config
Epoch:		1
Version:	2.10.1
Release:	4
Summary:	XKB data files
License:	MIT
Group:		Development/X11
URL:		http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source0:	http://www.x.org/releases/individual/data/xkeyboard-config/xkeyboard-config-%{version}.tar.bz2
Patch0:		xkeyboard-config-2.10.1-fixkbd.patch
# (Anssi 09/2008) Add fi(kotoistus_classic_nbsp) and use that by default.
# It has nbsp in level4 instead of level3 to avoid typos, as in fi(classic).
# See http://bugs.freedesktop.org/show_bug.cgi?id=12764
# Comments have been sent to the Kotoistus project.
Patch1:		xkeyboard-config-2.10.1-fi-kotoistus_classic_nbsp.patch

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
Patch2:		xkbdata-1.0.1-newkbd.patch
Patch3:		xkb-fix_uz.patch

# (fc) 1.5-2mdv map key_battery, wlan, bluetooth, uwb to their XF86 keycodes (GIT)
Patch6:		xkeyboard-config-1.4-battery.patch
# Revert change that disables zapping by default
Patch9:		xkeyboard-config-2.8-Enable-zapping-by-default.patch

#Add Altai and fix some Russia national layout
Patch10:	xkeyboard-config-2.7-altai.patch

# Add Swiss-German layout with ¨ deadkey, but without turning important
# development characters like ` or ' into deadkeys
Patch11:	xkeyboard-config-ch-scriptdeadkeys.patch

Patch12:	xkeyboard-config-2.10.1-br-support.diff

BuildRequires:	pkgconfig(x11)
BuildRequires:	glib-gettextize
BuildRequires:	intltool
BuildRequires:	perl-XML-Parser
BuildRequires:	x11-proto-devel
BuildRequires:	x11-util-macros
BuildRequires:	xkbcomp
# For the mab page
BuildRequires:	xsltproc
# https://qa.mandriva.com/show_bug.cgi?id=44052
BuildRequires:	gettext-devel

BuildArch:	noarch

%description
Xkeyboard-config provides consistent, well-structured, frequently released of X
keyboard configuration data (XKB) for various X Window System implementations.

%package -n %{old_name}
Summary:	%{summary}
Group:		%{group}

%description -n %{old_name}
Xkeyboard-config provides consistent, well-structured, frequently released of X
keyboard configuration data (XKB) for various X Window System implementations.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch6 -p1 -b .battery
#patch9 -p1 -b .enable-zapping
%patch10 -p1 -b .russain_national
%patch11 -p1 -b .ch_scriptdeadkeys
%patch12 -p1 -b .br

# fix build
aclocal
autoconf

%build
%configure2_5x \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --with-xkb-rules-symlink=xorg \
    --disable-runtime-deps

%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_localstatedir}/lib/xkb
#need this symlink for xkb to work (Mdv bug #34195)
ln -snf %{_localstatedir}/lib/xkb %{buildroot}%{_datadir}/X11/xkb/compiled

%find_lang %{name}

%pre -n %{old_name}
# this was a directory in the old installation
if [ -d "%{_datadir}/X11/xkb/compiled" ]; then
	rm -rf %{_datadir}/X11/xkb/compiled
fi

%files -f %{name}.lang -n %{old_name}
%dir %{_datadir}/X11/xkb/
%attr(1777,root,root) %dir %{_localstatedir}/lib/xkb
%{_datadir}/X11/xkb/*
%{_datadir}/pkgconfig/xkeyboard-config.pc
%{_mandir}/man7/xkeyboard-config.7.*
