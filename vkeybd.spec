%define name	vkeybd
%define version	0.1.17
%define release %mkrel 5

Summary:	Virtual ALSA MIDI keyboard
Name:		%name
Version:	%version
Release:	%release
License:	GPL
Group:		Sound
URL:		http://members.tripod.de/iwai/awedrv.html
Source:		http://www.alsa-project.org/~iwai/%{name}-%{version}.tar.bz2
Requires:	tk tcl
BuildRequires:	tk tk-devel tcl tcl-devel
BuildRequires:  X11-devel
BuildRequires:  alsa-lib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Vkeybd is a virtual keyboard (as in musical instrument)
for AWE32/64, raw MIDI, and ALSA sequencer drivers.  It is written in
Tcl/Tk.  Enjoy playing music with your "computer" keyboard :-)

%prep
%setup -n %{name}
perl -p -i -e "s|-O|$RPM_OPT_FLAGS||g" Makefile

%build
TCL_VERSION=$(echo 'puts [package require Tcl]' | tclsh)
make PREFIX=%{_prefix} \
	TCLLIB=-ltcl$TCL_VERSION \
	TKLIB=-ltk$TCL_VERSION \
	XLIB="-L/usr/X11R6/lib64 -L/usr/X11R6/lib -lX11"

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX="$RPM_BUILD_ROOT"%{_prefix} install
make MAN_DIR=$RPM_BUILD_ROOT%{_mandir} install-man

#menu
(cd $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Name=VKeybd
Comment=On-screen ALSA MIDI keyboard
Icon=%name
Categories=Audio;
EOF
)

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cp pixmaps/%{name}_48x48.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cp pixmaps/%{name}_32x32.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cp pixmaps/%{name}_16x16.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%update_menus

%files
%defattr(-,root,root)
%doc README ChangeLog
%{_bindir}/*
%{_datadir}/%name
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%name.desktop
%_iconsdir/%name.png
%_liconsdir/%name.png
%_miconsdir/%name.png

