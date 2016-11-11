# NOTE
# - stupid generic name, should be renamed
#   using upstream package name for now:
#   # sudo apt-get install serviced
#   http://controlcenter.io/gettingstarted.html

Summary:	Serviced is a PaaS runtime
Name:		serviced
Version:	1.1.9
Release:	0.1
License:	Apache v2.0
Group:		Applications/Networking
Source0:	https://github.com/control-center/serviced/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	85cd12444c9bddfe3c2bed82c70295cd
URL:		https://github.com/control-center/serviced
BuildRequires:	golang >= 1.4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/control-center/%{name}

%description
Serviced is a PaaS runtime. It allows users to create, manage and
scale services in a uniform way.

%prep
%setup -qc

ln -s Godeps/_workspace/src .
ln -s ../../../../.. src/%{import_path}

%build
export GOPATH=$(pwd)
cd src/%{import_path}

gov=$(go version | awk '{print $3}')
%{__make} \
	prefix=%{_prefix} \
	sysconfdir=%{_sysconfdir} \
	EXPECTED_GO_VERSION=$gov

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -p bin/%{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
