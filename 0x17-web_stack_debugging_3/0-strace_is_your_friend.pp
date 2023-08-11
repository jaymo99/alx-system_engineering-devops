# Fix typo in Wordpress settings file

exec { 'fix-wordpress':
  command => 'sed -i s/phpp/php/g /var/www/html/wp-settings.php',
  path    => '/usr/local/bin/:/bin/'
}

# notify Apache service to reload after PHP module is updated:
service { 'apache2':
  ensure => 'running',
  notify => Exec['fix-wordpress'],
}
