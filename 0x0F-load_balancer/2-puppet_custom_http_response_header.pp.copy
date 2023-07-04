# Installation and Configuration of Nginx in Ubuntu
exec { 'update':
  command => '/usr/bin/env apt-get -y update',
}

package { 'nginx' :
  ensure  => installed,
  require => Exec['update'],
}

# Create index.html file
file { 'index.html' :
  ensure  => present,
  path    => '/var/www/html/index.html',
  content => 'Hello World!',
  require => Package['nginx'],
}

# Add a custom HTTP header
file_line { 'custom_http_header':
  path    => '/etc/nginx/nginx.conf',
  after   => 'http {',
  line    => 'add_header X-Served-By $hostname;',
  notify  => Exec['restart_nginx'],
  require => Package['nginx'],
}

# NGINX service
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

# Restart NGINX service
exec { 'restart_nginx':
  command     => '/usr/sbin/service nginx restart',
  refreshonly => true,
  require => Package['nginx'],
}
