%global name        oval-graph
%global module      oval_graph

Summary:            Tool for visualization of SCAP rule evaluation results
Name:               %{name}
Version:            1.0.1
Release:            1%{?dist}
# The entire source code is ASL 2.0 except schemas/ which is Public Domain
License:            ASL 2.0 and Public Domain

Url:                https://pypi.org/project/%{name}/
Source0:            https://files.pythonhosted.org/packages/source/o/%{name}/%{module}-%{version}.tar.gz

BuildArch:          noarch

BuildRequires:      python3-devel

%description
Oval_graph is a tool that displays the results of evaluating SCAP rules.
In the form of a tree according to the OVAL standard. Using the
`arf-to-graph` command, you can simply view the result of rule.
Use `arf-to-json` to generate a rule result in json. Using the
`json-to-graph` command, you can view the results of rules from json file.

%{?python_enable_dependency_generator}

%prep
%autosetup -n %{module}-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{module}/
%{python3_sitelib}/%{module}-*.egg-info/
%{_bindir}/arf-to-graph
%{_bindir}/arf-to-json
%{_bindir}/json-to-graph

%changelog
* Mon Mar 09 2020 Jan Rodak <jrodak@redhat.com> - 1.0.1-1
- release 1.0.1

* Mon Mar 09 2020 Jan Rodak <jrodak@redhat.com> - 1.0.0-1
- release 1.0.0

* Wed Jan 22 2020  Jan Rodak <jrodak@redhat.com> - 0.1.2-1
- Improved performance
- New commands

* Wed Nov 13 2019  Jan Rodak <jrodak@redhat.com> - 0.0.2-1
- Changed CR+LF to LF line endings.

* Wed Oct 23 2019  Jan Rodak <jrodak@redhat.com> - 0.0.1-1
- Initial version of the package.

