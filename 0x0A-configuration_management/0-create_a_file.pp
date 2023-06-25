# create a file in /tmp

$tmp_dir = '/tmp'

file { "${tmp_dir}/school":
  ensure  => 'present',
  mode    => '0744',
  owner   => 'www-data',
  group   => 'www-data',
  content => 'I love Puppet',
}
