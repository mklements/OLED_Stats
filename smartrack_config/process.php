<?php 

$ip_address = $_POST['ip_address'];
$gateway =  $_POST['gateway'];

$output = shell_exec("sudo /home/smartrack/smartrack-pi/.venv/bin/python /home/smartrack/smartrack-pi/smartrack_pi/cli.py net static $ip_address $gateway") or die("Failed Running static change");

exit;
?>