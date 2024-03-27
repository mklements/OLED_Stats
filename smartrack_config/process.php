<?php 
error_reporting(E_ALL);

$ip_address = $_POST['ip_address'];
$gateway = $_POST['gateway'];
// Open the file for writing
$filename = '/home/smartrack/smartrack-pi/smartrack_pi/.env';

$file = fopen($filename, 'w'); 

$content = "STATIC_IP=$ip_address\nGATEWAY=$gateway";
// Write new data to the file
fwrite($file, "$content");

// Close the file
fclose($file);

echo "IP Set to: $ip_address!, Gateway Set to: $gateway";

?>