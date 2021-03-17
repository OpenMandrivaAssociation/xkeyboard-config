%define git_url git://anongit.freedesktop.org/xkeyboard-config

Name:		xkeyboard-config
Epoch:		1
Version:	2.32
Release:	2
Summary:	X Keyboard Configuration Database
License:	MIT
Group:		Development/X11
URL:		http://www.freedesktop.org/wiki/Software/XKeyboardConfig
Source0:	http://www.x.org/releases/individual/data/xkeyboard-config/%{name}-%{version}.tar.bz2
Source1:	xkeyboard-config.rpmlintrc
BuildRequires:	meson
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

%build
%meson -Dcompat-rules=true
%meson_build

%install
%meson_install

# need this symlink for xkb to work (Mdv bug #34195)
mkdir -p %{buildroot}%{_localstatedir}/lib/xkb
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
