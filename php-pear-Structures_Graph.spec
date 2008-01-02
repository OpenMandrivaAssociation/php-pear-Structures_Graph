%define		_class		Structures
%define		_subclass	Graph
%define		_status		stable
%define		_pearname	%{_class}_%{_subclass}

%define         _requires_exceptions pear(PHPUnit.php)

Summary:	%{_pearname} - graph datastructure manipulation library
Name:		php-pear-%{_pearname}
Version:	1.0.2
Release:	%mkrel 2
License:	LGPL
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/Structures_Graph/
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRequires:	recode
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Structures_Graph is a package for creating and manipulating graph
datastructures. It allows building of directed and undirected graphs,
with data and metadata stored in nodes. The library provides functions
for graph traversing as well as for characteristic extraction from the
graph topology.

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

# fix bad xml
recode -d latin-1..html < package.xml > package.xml~
mv package.xml~ package.xml

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Manipulator

install %{_pearname}-%{version}/%{_class}/*.php %{buildroot}%{_datadir}/pear/%{_class}
install %{_pearname}-%{version}/%{_class}/%{_subclass}/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/
install %{_pearname}-%{version}/%{_class}/%{_subclass}/Manipulator/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Manipulator

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_pearname}-%{version}/tests %{_pearname}-%{version}/LICENSE
%{_datadir}/pear/%{_class}/*.php
%{_datadir}/pear/%{_class}/%{_subclass}
%{_datadir}/pear/packages/%{_pearname}.xml
