<html>
<head>
 <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
<h2>Raspberry Pi Temperature Data</h2>
<div id='chart_div'></div>
<?PHP
# Open Sqlite database
try {
 $db = new SQLite3('/home/pi/Labs/lab8/temperature.db');
}
catch (Exception $exception) {
 echo '<p>There was an error connecting to the database!</p>';
}
?>
<script>
var data = [{
 x: [
<?PHP
 # Use PHP to query database and build JavaScript array
 $query = 'SELECT * FROM TemperatureData';
 $result = $db->query($query) or die('Query failed');
 while ($row = $result->fetchArray()) {
 echo " '" . $row['datetime'] . "',\n";
 }
?>
 ],
 y: [
<?PHP
 while ($row = $result->fetchArray()) {
 echo " " . $row['temperature'] . ",\n";
 }
?>
 ],
 type: 'scatter'
}];
var layout = {
 xaxis: { title: 'Date and time' },
 yaxis: { title: 'Temperature (degrees C)' }
};
Plotly.newPlot('chart_div', data, layout );
</script>
</body>
</html>
