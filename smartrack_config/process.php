<?php 

$ip_address = $_POST['ip_address'];
$gateway =  $_POST['gateway'];

$output = shell_exec("sudo /home/smartrack/smartrack-pi/.venv/bin/python /home/smartrack/smartrack-pi/smartrack_pi/cli.py static $ip_address $gateway") or die("Failed Running static change");
$filename = '/home/smartrack/smartrack-pi/smartrack_pi/config.json';
$config["static_ip"] =$ip_address;
$config["gateway"]  =$gateway;
$config["mode"] = "S";
$json = json_encode($config);
file_put_contents($filename, $json) or die("Failed Writing JSON");
exit;
?>