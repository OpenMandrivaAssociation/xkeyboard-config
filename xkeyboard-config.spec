%define git_url git://anongit.freedesktop.org/xkeyboard-config

Name:		xkeyboard-config
Epoch:		1
Version:	2.30
Release:	1
Summary:	X Keyboard Configuration Database
License:	MIT
Group:		Development/X11
URL:		http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source0:	http://www.x.org/releases/individual/data/xkeyboard-config/%{name}-%{version}.tar.bz2
Source1:	xkeyboard-config.rpmlintrc
Patch0:		xkeyboard-config-2.17-fixkbd.patch
# (Anssi 09/2008) Add fi(kotoistus_classic_nbsp) and use that by default.
# It has nbsp in level4 instead of level3 to avoid typos, as in fi(classic).
# See http://bugs.freedesktop.org/show_bug.cgi?id=12764
# Comments have been sent to the Kotoistus project.
Patch1:		xkeyboard-config-2.10.1-fi-kotoistus_classic_nbsp.patch

Patch3:		xkb-fix_uz.patch

# Revert change that disables zapping by default
#Patch9:		xkeyboard-config-2.8-Enable-zapping-by-default.patch

#Add Altai and fix some Russia national layout
#Patch10:	xkeyboard-config-2.11-altai.patch

# Add Swiss-German layout with ¨ deadkey, but without turning important
# development characters like ` or ' into deadkeys
Patch11:	xkeyboard-config-ch-scriptdeadkeys.patch
# (tpg) rediff if you like it
#Patch12:	xkeyboard-config-2.10.1-br-support.patch

# (tpg) patches from Debian
# https://salsa.debian.org/xorg-team/data/xkb-data/tree/debian-unstable/debian/patches
#Patch20:	revert-Map-evdev-keycode-KEY_BRIGHTNESS_CYCLE.diff
#Patch21:	revert-Map-evdev-keycode-KEY_KEYBOARD.diff
#Patch22:	revert-Map-evdev-keycode-KEY_FAVORITES.diff
BuildRequires:	pkgconfig(x11)
BuildRequires:	glib-gettextize
BuildRequires:	intltool
BuildRequires:	perl-XML-Parser
BuildRequires:	x11-proto-devel
BuildRequires:	x11-util-macros
BuildRequires:	xkbcomp
# For the man page
BuildRequires:	xsltproc
# https://qa.mandriva.com/show_bug.cgi?id=44052
BuildRequires:	gettext-devel
%rename		x11-data-xkbdata
BuildArch:	noarch

%description
Xkeyboard-config provides consistent, well-structured, frequently released of X
keyboard configuration data (XKB) for various X Window System implementations.

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}

%description devel
Development files for %{name}.

%prep
%autosetup -p1

# fix build
aclocal
autoconf

%build
%configure \
    --enable-compat-rules \
    --with-xkb-base=%{_datadir}/X11/xkb \
    --with-xkb-rules-symlink=xorg \
    --disable-runtime-deps

%make_build

%install
%make_install

mkdir -p %{buildroot}%{_localstatedir}/lib/xkb
#need this symlink for xkb to work (Mdv bug #34195)
ln -snf %{_localstatedir}/lib/xkb %{buildroot}%{_datadir}/X11/xkb/compiled

%find_lang %{name}

%triggerin -- %{name} < 1:2.23.1-2
# this was a directory in the old installation
if [ -d "%{_datadir}/X11/xkb/compiled" ]; then
    rm -rf %{_datadir}/X11/xkb/compiled
fi

%files -f %{name}.lang
%dir %{_datadir}/X11/xkb/
%attr(1777,root,root) %dir %{_localstatedir}/lib/xkb
%{_datadir}/X11/xkb/*
%{_mandir}/man7/xkeyboard-config.7.*

%files devel
%{_datadir}/pkgconfig/xkeyboard-config.pc
