# Installation and Configuration of Nginx in Ubuntu
exec { 'update':
  command => '/usr/bin/env apt-get -y update',
}

package { 'nginx' :
  ensure  => installed,
  require => Exec['update'],
}

# Add a custom HTTP header
file_line { 'custom_http_header':
  path    => '/etc/nginx/nginx.conf',
  after   => 'http {',
  line    => "\tadd_header X-Served-By \$hostname;",
  notify  => Exec['restart_nginx'],
  require => Package['nginx'],
}

# Create index.html file
file { 'index.html' :
  ensure  => present,
  path    => '/var/www/html/index.html',
  content => 'Hello World!',
  require => Package['nginx'],
}

# Create custom 404.html file
file { '404.html' :
  ensure  => present,
  path    => '/var/www/html/404.html',
  content => 'Ceci n\'est pas une page',
  require => Package['nginx'],
}

file_line { '404_error_page':
  path    => '/etc/nginx/sites-available/default',
  after   => 'server_name _;',
  line    => "\terror_page 404 /404.html;",
  notify  => Exec['restart_nginx'],
  require => File['404.html'],
}

# Add redirection rule
file_line { 'nginx-redirection-rule':
  path    => '/etc/nginx/sites-available/default',
  after   => 'server_name _;',
  line    => "\trewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;",
  notify  => Exec['restart_nginx'],
  require => File['index.html'],
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
}
