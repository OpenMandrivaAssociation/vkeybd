Summary:	Virtual ALSA MIDI keyboard
Name:		vkeybd
Version:	0.1.17b
Release:	%mkrel 4
License:	GPLv2+
Group:		Sound
URL:		http://www.alsa-project.org/~tiwai/alsa.html
# From Debian as there appears to be no upstream source I can find,
# though this is a genuine release made by the author as he referred
# to it in a Debian bug report. - AdamW 2008/01
Source:		http://ftp.de.debian.org/debian/pool/main/v/vkeybd/%{name}_%{version}.orig.tar.gz
Requires:	tk
Requires:	tcl
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:  X11-devel
BuildRequires:  alsa-lib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Vkeybd is a virtual keyboard (as in musical instrument)
for AWE32/64, raw MIDI, and ALSA sequencer drivers.  It is written in
Tcl/Tk.  Enjoy playing music with your "computer" keyboard :-)

%prep
%setup -q -n %{name}
perl -p -i -e "s|-O|$RPM_OPT_FLAGS||g" Makefile

%build
TCL_VERSION=8.5
make PREFIX=%{_prefix} \
	TCLLIB=-ltcl$TCL_VERSION \
	TKLIB=-ltk$TCL_VERSION \
	XLIB="-lX11"

%install
rm -rf %{buildroot}
make PREFIX="%{buildroot}"%{_prefix} install
make MAN_DIR=%{buildroot}%{_mandir} install-man

#menu
(cd %{buildroot}
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Name=VKeybd
Comment=On-screen ALSA MIDI keyboard
Icon=%{name}
Categories=Audio;
EOF
)

#icons
mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
cp pixmaps/%{name}_48x48.png %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png
cp pixmaps/%{name}_32x32.png %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
cp pixmaps/%{name}_16x16.png %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{update_menus}
%{clean_icon_cache hicolor}
%endif

%files
%defattr(-,root,root)
%doc README ChangeLog
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

