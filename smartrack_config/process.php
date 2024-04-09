<?php 
$filename = '/home/smartrack/smartrack-pi/smartrack_pi/config.json';
$json = file_get_contents($filename);
$config = json_decode($json, true);

$config["static_ip"] = $_POST['ip_address'];
$config["gateway"]  = $_POST['gateway'];
$config["mode"] = "S";
$json = json_encode($config);
file_put_contents($filename, $json) or die("asdfjk");

// $command = "smartrackcli dhcp";
// $output = shell_exec($command);
// echo $output

header("Location: index.php");
exit;
?>