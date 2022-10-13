%define git_url git://anongit.freedesktop.org/xkeyboard-config

Name:		xkeyboard-config
Epoch:		1
Version:	2.37
Release:	1
Summary:	X Keyboard Configuration Database
License:	MIT
Group:		Development/X11
URL:		http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source0:	http://www.x.org/releases/individual/data/xkeyboard-config/%{name}-%{version}.tar.xz
Source1:	xkeyboard-config.rpmlintrc
BuildRequires:	meson
BuildRequires:	gettext-devel
BuildRequires:	glib-gettextize
BuildRequires:	intltool
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

%triggerin -- %{name} < 1:2.23.1-2
# this was a directory in the old installation
if [ -d "%{_datadir}/X11/xkb/compiled" ]; then
    rm -rf %{_datadir}/X11/xkb/compiled
fi

%files -f files.list -f %{name}.lang
%doc AUTHORS README NEWS COPYING docs/README.* docs/HOWTO.*
%doc %{_mandir}/man7/xkeyboard-config.*
%{_datadir}/X11/xkb/rules/xorg
%{_datadir}/X11/xkb/rules/xorg.lst
%{_datadir}/X11/xkb/rules/xorg.xml

%files devel
%{_datadir}/pkgconfig/xkeyboard-config.pc
