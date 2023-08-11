# Fix file typo in Wordpress settings file
exec { 'fix_settings_file':
  command => 'sed -i "s/phpp/php/g" /var/www/html/wp-settings.php',
}
