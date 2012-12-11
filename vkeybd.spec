Summary:	Virtual ALSA MIDI keyboard
Name:		vkeybd
Version:	0.1.18d
Release:	%mkrel 6
License:	GPLv2+
Group:		Sound
URL:		http://www.alsa-project.org/~tiwai/alsa.html
# From Debian as there appears to be no upstream source I can find,
# though this is a genuine release made by the author as he referred
# to it in a Debian bug report. - AdamW 2008/01
Source0:	http://ftp.de.debian.org/debian/pool/main/v/vkeybd/%{name}_%{version}.orig.tar.gz
Requires:	tk
Requires:	tcl
BuildRequires:	tk
BuildRequires:	pkgconfig(tk)
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:  alsa-oss-devel

%description
Vkeybd is a virtual keyboard (as in musical instrument)
for AWE32/64, raw MIDI, and ALSA sequencer drivers.  It is written in
Tcl/Tk.  Enjoy playing music with your "computer" keyboard :-)

%prep
%setup -q
perl -p -i -e "s|-O|%optflags||g" Makefile

%build
make PREFIX=%{_prefix} \
	TCLLIB=-ltcl%{tcl_version} \
	TKLIB=-ltk%{tcl_version} \
	CC="gcc %ldflags"

%install
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

%files
%doc README ChangeLog
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
