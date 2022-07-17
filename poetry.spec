Name:           poetry
Summary:        Python dependency management and packaging made easy
Version:        1.1.14
Release:        1
License:        MIT
 
URL:            https://python-poetry.org/
Source0:        https://github.com/python-poetry/poetry/archive/%{version}/poetry-%{version}.tar.gz
 
BuildArch:      noarch
 
BuildRequires:  pkgconfig(python)

# The tests deps are only defined as part of poetry.dev-dependencies together with tox, pre-commit etc.
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  python-pip
BuildRequires:  python-wheel
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(httpretty)
BuildRequires:  python3dist(virtualenv)
 
Requires:       python-poetry = %{version}-%{release}
 
%description
Poetry helps you declare, manage and install dependencies of Python projects, ensuring you have the right stack everywhere.
It requires Python 3.7+ to run.
 
 
%package -n     python-poetry
Summary:        %{summary}
%description -n python-poetry
Poetry helps you declare, manage and install dependencies of Python projects, ensuring you have the right stack everywhere.
It requires Python 3.7+ to run.
 
%prep
%autosetup -p1
 
# remove vendored dependencies
#rm -r poetry/_vendor
 
mkdir wheels
pip wheel --wheel-dir wheels --no-deps --no-build-isolation --verbose .

%install
pip install --root=%{buildroot} --no-deps --verbose --ignore-installed --no-warn-script-location --no-index --no-cache-dir --find-links wheels wheels/*.whl
 

%files
%{_bindir}/poetry
# The directories with shell completions are co-owned
%{_datadir}/bash-completion/
%{_datadir}/fish/
%{_datadir}/zsh/
 
 
%files -n python-poetry
%license LICENSE
%doc README.md
