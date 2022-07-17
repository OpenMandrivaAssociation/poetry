Name:           poetry
Summary:        Python dependency management and packaging made easy
Version:        1.1.13
Release:        1
License:        MIT
 
URL:            https://python-poetry.org/
Source0:        https://github.com/python-poetry/poetry/archive/%{version}/poetry-%{version}.tar.gz
 
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
 
# The tests deps are only defined as part of poetry.dev-dependencies together with tox, pre-commit etc.
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  /usr/bin/python
BuildRequires:  %py3_dist pytest
BuildRequires:  %py3_dist pytest-mock
BuildRequires:  %py3_dist httpretty
BuildRequires:  %py3_dist virtualenv
 
Requires:       python3-poetry = %{version}-%{release}
 
%description %{common_description}
 
 
%package -n     python3-poetry
Summary:        %{summary}
%description -n python3-poetry %{common_description}
 
 
%prep
%autosetup -p1
 
# remove vendored dependencies
rm -r poetry/_vendor
 
# compatibility with more pytest-mock versions
sed -i s/MockFixture/MockerFixture/ tests/repositories/test_installed_repository.py
 
# New empty projects created by poetry have a default dev dependency on pytest ^5.2,
# however that version is not compatible with Python 3.10.
# Hence, we replace it with a known compatible version 6.2 instead.
# Upstream has already removed the default pytest dependency in 1.2.0a1+,
# this sed should be removed once we update.
%if v"%{python3_version}" >= v"3.10"
    sed -i 's/5\.2/6\.2/' poetry/console/commands/new.py
%endif
 
# Allow newer packaging version
# https://github.com/python-poetry/poetry/issues/4264
sed -i 's/packaging = "^.*"/packaging = "*"/' pyproject.toml
 
%generate_buildrequires
%pyproject_buildrequires -r
 
 
%build
%pyproject_wheel
 
%install
%pyproject_install
%pyproject_save_files poetry
 
export PYTHONPATH=%{buildroot}%{python3_sitelib}
for i in bash,bash-completion/completions,poetry fish,fish/vendor_completions.d,poetry.fish zsh,zsh/site-functions,_poetry; do IFS=","
    set -- $i
    mkdir -p %{buildroot}%{_datadir}/$2
    # poetry leaves references to the buildroot in the completion files -> remove them
    %{buildroot}%{_bindir}/poetry completions $1 | sed 's|%{buildroot}||g' > %{buildroot}%{_datadir}/$2/$3
done
 
%check
# don't use %%tox here because tox.ini runs "poetry install"
# test_lock_no_update: attempts a network connection to pypi
# test_export_exports_requirements_txt_file_locks_if_no_lock_file:
#    virtualenv: error: argument dest: the destination . is not write-able at /
# test_executor and test_editable_builder doesn't work with pytest7
#    upstream report: https://github.com/python-poetry/poetry/issues/4901
%pytest -k "not lock_no_update and \
not export_exports_requirements_txt_file_locks_if_no_lock_file and \
not executor and \
not editable_builder"
 
 
%files
%{_bindir}/poetry
# The directories with shell completions are co-owned
%{_datadir}/bash-completion/
%{_datadir}/fish/
%{_datadir}/zsh/
 
 
%files -n python3-poetry -f %{pyproject_files}
%license LICENSE
%doc README.md
