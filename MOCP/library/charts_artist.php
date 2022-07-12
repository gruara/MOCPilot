<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>
<?php 

$artist='';


$errormessage='';
$errors=false;
$initial_load=true;
?>
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>

<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/charts_left_menu.inc.php' ?>
</div>

<div style="margin-left:20%">
<?php 

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	if (empty($_POST['artist'])) {
		$_SESSION['last_artist']='';
	} else {
		$artist=$_POST['artist']; 
		$_SESSION['last_artist']=$_POST['artist']; 
	}
	
	if ( $errormessage == '') {
		if (isset($_POST['exact']))
			{
				$exact=", \"exact\" : \"true\"";
			} else {
				$exact ="";
			}
		$payload = "{ \"artist\" : \"{$artist }\" $exact}";
		$response = run_web_service('chart_artist', $payload, 'GET');
		$reply=json_decode($response,true);

	};
};
?><form <form class="w3-container" method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
<div class="w3-container w3-center "> <h2><?php echo 'Artist Hits';?></h2> </div>
<div class="w3-row-padding">
  <div style="width:80%">
  <label for="artist">Artist:</label>  
  <input class="w3-input" type="text" id="artist" name="artist" style="width:50%">
  <label>Exact Match	
  <input class="w3-check" type="checkbox"  id="exact" name="exact" style="width:5%">
  </label>
  </div>
 
  <div class="w3-third" style="width:10%" >
	<input class="w3-button w3-light-grey w3-round-large w3-medium"  type="submit" value="List">
  </div>
 
  <div class="w3-third" >
	<?php echo $errormessage ?>
  </div>	
</div>
</form>

<div></div>
<div class="w3-responsive" >
  <table class="w3-table w3-striped w3-small" style="width:80%">
    <tr style="width:100%">
      <th style="width:20%" >Artist </th>
      <th style="width:30%" >Title</th>
	  <th style="width:10%" >First Entry</th>
	  <th style="width:10%" >Last Entry</th>
	  <th style="width:10%" >Weeks on Chart</th>
	  <th style="width:10%" >Highest</th>

<?php
if (($_SERVER["REQUEST_METHOD"] == "POST") ) {
	
 // TODO Standardise response handling from web services
 	if ($reply[1]['http_reply']['http_code'] != 200) {

			echo'<tr>  No jobs matching supplied criteria</tr>';
		} else {
			foreach ($reply[0] as $job) {

				$payload = "{ \"artist\" : \"{$job['artist']}\",
							  \"song\" : \"{$job['song'] }\"}";

				$response = run_web_service('chart_song_summary', $payload, 'GET');

				$reply=json_decode($response,true);
                                                                           
				$dets=$reply[0];
				
				echo "<tr margin='none'>
				      
					   <td> {$job['artist']} </td>
					   <td> {$job['song']} </td>
					   <td> {$dets[0]['earliest_date']} </td>
					   <td> {$dets[0]['latest_date']} </td>
					   <td> {$dets[0]['weeks_on_chart']} </td>
					   <td> {$dets[0]['highest_position']} </td>
					  	
					 </tr>";
			};
		};
		$initial_load=false;
	};
?>
</div></div>
</table>
</body>

</html>