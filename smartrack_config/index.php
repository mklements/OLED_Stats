<!DOCTYPE html>
<html>
    <body>
        <h1>CT Smartrack</h1>
        <p>Enter static ip address in slash notation. i.e 192.168.1.201/24 for subnet mask of 255.255.255.0</p>
        <form action="process.php" method="post">
            <label for="ip_address">IP:</label>
            <input type="text" id="ip_address" name="ip_address" /><br /><br />
            <label for="gateway">Gateway:</label>
            <input type="text" id="gateway" name="gateway" /><br /><br />
            <input type="submit" value="Submit" />
        </form>
    </body>
</html>
