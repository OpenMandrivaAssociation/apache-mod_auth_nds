#Module-Specific definitions
%define mod_name mod_auth_nds
%define mod_conf 98_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	2.0
Release:	17
Group:		System/Servers
License:	GPL
URL:		https://www.gknw.com/development/apache/
Source0: 	http://www.gknw.com/development/apache/httpd-2.0/unix/modules/%{mod_name}-%{version}beta.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_auth_nds-2.0-register.patch
Patch1:		mod_auth_nds-2.0-apache220.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	ncpfs-devel
BuildRequires:	file
Epoch:		1

%description
mod_auth_nds is the Novell(tm) NDS(tm) authentication module for 
the apache web server.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c %{mod_name}.c -I%{_includedir}/ncp -lncp 

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc my_cfg.txt ChangeLog INSTALL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-16mdv2012.0
+ Revision: 772564
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-15
+ Revision: 678264
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-14mdv2011.0
+ Revision: 587922
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-13mdv2010.1
+ Revision: 516048
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-12mdv2010.0
+ Revision: 406536
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-11mdv2009.0
+ Revision: 234661
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-10mdv2009.0
+ Revision: 215533
- fix rebuild

* Sat Mar 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-9mdv2008.1
+ Revision: 182105
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:2.0-8mdv2008.1
+ Revision: 170705
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request
- rebuild b/c of missing package on ia32

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-6mdv2008.0
+ Revision: 82521
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-5mdv2008.0
+ Revision: 65623
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0-4mdv2007.1
+ Revision: 140611
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-3mdv2007.1
+ Revision: 79326
- Import apache-mod_auth_nds

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-3mdv2007.0
- rebuild

* Thu Dec 15 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-2mdk
- rebuilt against apache-2.2.0 (P1)

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-1mdk
- fix versioning
- fix url

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-5mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-4mdk
- fix %%post and %%postun to prevent double restarts

* Fri Feb 25 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_2.0-3mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.0-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_2.0-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.0-0.beta.1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_2.0-0.beta.1mdk
- built for apache 2.0.49

