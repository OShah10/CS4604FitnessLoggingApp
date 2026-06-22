<?php
    $host = 'localhost';
    $username = 'logan';
    $password = 'password';
    $dbname = "sailing";
    $connect = mysqli_connect($host, $username, $password, "$dbname");

    if (!$connect){
        die('Could not connect to MySQL Server:' .mysqli_error());
    }

    $searchTerm = $_POST['searchterm'];
    $query = "SELECT * FROM SHIP WHERE S_Name = '{$searchTerm}';";

    $result = mysqli_query($connect, $query);

    if ($result->num_rows >0){
        while ($row = $result->fetch_assoc()){
            echo "<h1> Search Results </h1>";
            echo "<p1> Your search term returned these results: </p1> <br>";
            echo "Ship Name: " . $row["S_Name"] . " Owner: " . $row["Owner"] . " Type: " . $row["Type"] . " Port Name: " . $row["P_Name"] . " State: " . $row["S_C_Name"];
        }
    }
        else{
            echo "No results found";
        }

    $connect->close();
?>


