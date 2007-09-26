%define pkgversion 1.1
Name: x11-data-xkbdata
Epoch: 1
Version: %{pkgversion}
Release: %mkrel 1
BuildArch: noarch
Summary: xkb data files
URL:   http://www.freedesktop.org/wiki/Software_2fXKeyboardConfig
Group: Development/X11
# cvs -d:pserver:anoncvs@cvs.freedesktop.org:/cvs/xkeyboard-config login
# <press enter>
# cvs -d:pserver:anoncvs@cvs.freedesktop.org:/cvs/xkeyboard-config co -r v_1_1 xkeyboard-config
Source: xkeyboard-config-%{pkgversion}.tar.bz2 

# symbols/kg and symbols/la besides looking very simple patches, did not apply
#   cleanly, so removed for now
# Dropped all conflicting patches
Patch0: xkbdata-1.0.1-fixkbd.patch

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

License: MIT
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: xkbcomp >= 1.0.1
BuildRequires: perl-XML-Parser
BuildRequires: intltool

%description
Xkeyboard-config provides consistent, well-structured, frequently released of X
keyboard configuration data (XKB) for various X Window System implementations.

%prep
%setup -q -n xkeyboard-config-%{pkgversion}

# Keyboard fixes patches -- pablo
%patch0 -p1 -b .fixkbd

	#   Not applied as most are already implemented, but in a compeletely
	#   different way. May need some review as described for Patch2:
	#   Still just keeping the old patch for reference in case problems
	#   arise.
# New keyboard layouts -- pablo
# %patch2 -p1 -b .newkbd

%patch4 -p1 -b .uz_fix

%build
./autogen.sh
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


