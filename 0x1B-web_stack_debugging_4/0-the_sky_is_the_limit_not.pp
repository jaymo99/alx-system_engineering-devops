exec { 'fix--for-nginx':
  command     => 'sed -i "s/-n 15/-n 4096/" /etc/default/nginx',
  path        => '/usr/local/bin/:/bin/',
  notify      => Service['nginx']
}

# Nginx restart
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  require   => Exec['fix--for-nginx'],
  subscribe => Exec['fix--for-nginx']
}
