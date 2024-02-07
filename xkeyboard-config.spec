# (tpg) Package contains data-only, no binaries, so no debuginfo is needed
%global debug_package %{nil}

Name:		xkeyboard-config
Epoch:		1
Version:	2.41
Release:	1
Summary:	X Keyboard Configuration Database
License:	MIT
Group:		Development/X11
URL:		https://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source0:	https://www.x.org/releases/individual/data/xkeyboard-config/%{name}-%{version}.tar.xz
Source1:	xkeyboard-config.rpmlintrc
BuildRequires:	meson
BuildRequires:	gettext-devel
BuildRequires:	glib-gettextize
BuildRequires:	intltool
BuildRequires:	locales-extra-charsets
# For the man page
BuildRequires:	xsltproc
BuildRequires:	xkbcomp
BuildRequires:	perl(XML::Parser)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xorg-macros)
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

%build
%meson -Dcompat-rules=true -Dxorg-rules-symlinks=true
%meson_build

%install
%meson_install

# Remove unnecessary symlink
rm -f %{buildroot}%{_datadir}/X11/xkb/compiled
%find_lang %{name}

# Create filelist
{
 FILESLIST=${PWD}/files.list
 cd %{buildroot}
 find .%{_datadir}/X11/xkb -type d | sed -e "s/^\./%dir /g" > $FILESLIST
 find .%{_datadir}/X11/xkb -type f | sed -e "s/^\.//g" >> $FILESLIST
 cd ..
}

%find_lang %{name}

%files -f files.list -f %{name}.lang
%doc AUTHORS README NEWS COPYING docs/README.* docs/HOWTO.*
%doc %{_mandir}/man7/xkeyboard-config.*
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml

%files devel
%{_datadir}/pkgconfig/xkeyboard-config.pc
