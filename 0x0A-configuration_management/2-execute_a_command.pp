# Kills a process named 'killmenow'

exec { 'pkill -9 killmenow':
  command => '/usr/bin/env pkill -9 killmenow',
}
