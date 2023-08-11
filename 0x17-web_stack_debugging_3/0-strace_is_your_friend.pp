# Fix file typo in Wordpress settings file

exec { 'fix_settings_file':
  command => 'sudo sed -i "s/.phpp/.php/g" /var/www/html/wp-settings.php',
  path    => '/usr/local/bin/:/bin/'
}
