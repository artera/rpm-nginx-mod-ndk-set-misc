%define _setmiscver         0.32
%define _ndkver             0.3.1

Summary: Various set_xxx directives added to nginx's rewrite + ngx_devel_kit
Name: nginx-mod-ndk-set-misc
Version: %{_ndkver}+%{_setmiscver}
Release: 1%{?dist}
Vendor: Artera
URL: https://github.com/openresty/set-misc-nginx-module

%define _nginxver           1.16.1
%define nginx_config_dir    %{_sysconfdir}/nginx
%define nginx_build_dir     %{_builddir}/nginx-%{_nginxver}

Source0: https://nginx.org/download/nginx-%{_nginxver}.tar.gz
Source1: https://github.com/openresty/set-misc-nginx-module/archive/v%{_setmiscver}/set-misc-%{_setmiscver}.tar.gz
Source2: https://github.com/simpl/ngx_devel_kit/archive/v%{_ndkver}/ngx_devel_kit-%{_ndkver}.tar.gz

Requires: nginx = 1:%{_nginxver}
BuildRequires: nginx
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: perl-devel
BuildRequires: gd-devel
BuildRequires: GeoIP-devel
BuildRequires: libxslt-devel
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: gperftools-devel

License: BSD

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Various set_xxx directives added to nginx's rewrite + ngx_devel_kit.

%prep
%setup -q -n nginx-%{_nginxver}
%setup -T -D -b 1 -n set-misc-nginx-module-%{_setmiscver}
%setup -T -D -b 2 -n ngx_devel_kit-%{_ndkver}

%build
cd %{_builddir}/nginx-%{_nginxver}
./configure %(nginx -V 2>&1 | grep 'configure arguments' | sed -r 's@^[^:]+: @@') --add-dynamic-module=../ngx_devel_kit-%{_ndkver} --add-dynamic-module=../set-misc-nginx-module-%{_setmiscver}
make modules

%install
%{__rm} -rf %{buildroot}

%{__install} -Dm755 %{nginx_build_dir}/objs/ndk_http_module.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ndk_http_module.so
%{__install} -Dm755 %{nginx_build_dir}/objs/ngx_http_set_misc_module.so \
    $RPM_BUILD_ROOT%{_libdir}/nginx/modules/ngx_http_set_misc_module.so

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*.so
