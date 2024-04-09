<!DOCTYPE html>

<?php
$json = file_get_contents('/home/smartrack/smartrack-pi/smartrack_pi/config.json');
$config = json_decode($json, true);
$static_ip = $data['static_ip']; 
$gateway = $data['gateway'];
$mode = $data['mode'];
?>

<html>
    <body>
        <h1>CT Smartrack</h1>
        <p>Enter static ip address in slash notation. i.e 192.168.1.201/24 for subnet mask of 255.255.255.0</p>
        <form action="process.php" method="post">
            <label for="ip_address">IP:</label>
            <input type="text" id="ip_address" name="ip_address" value="<?php echo $static_ip; ?>" /><br /><br />
            <label for="gateway">Gateway:</label>
            <input type="text" id="gateway" name="gateway" value="<?php echo $gateway; ?>" /><br /><br />
            <input type="submit" value="Submit" />
        </form>
    </body>
</html>