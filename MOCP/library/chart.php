<html>
<?php 
   session_start();
   $_SESSION["suite"]='Charts'; 
   $_SESSION['last_chart_date']="";
   $errormessage='';
    $errors=false;
?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>

<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/charts_left_menu.inc.php' ?>
</div>

<div style="margin-left:25%">

<?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        if (empty($_POST['chart_date']))  {
          $_SESSION['last_chart_date']='';
        } else {
          $chart_date=$_POST['chart_date']; 
          $_SESSION['last_chart_date']=$_POST['chart_date'];
        }

        $payload = "{ \"chart_date\" : \"$chart_date\" }";

        $response = run_web_service('chart_id', $payload, 'GET');
        $reply=json_decode($response,true);
        $dets=$reply[0];
        $chart_id = $dets[0]['chart_id'];

        $payload = "{ \"chart_id\" : \"$chart_id\" }";
        $response = run_web_service('chart', $payload, 'GET');
        $reply=json_decode($response,true);
    }
?>
<form <form class="w3-container" method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
<div class="w3-third" style="width:15%">
   <input type="text" class="w3-input " maxlength="10" id="chart_date" name="chart_date" value="<?php echo  $_SESSION['last_chart_date']?>" placeholder="SCHEDULE DATE">
 </div>


  <div class="w3-third" style="width:10%" >
	<input class="w3-button w3-light-grey w3-round-large w3-medium"  type="submit" value="Submit">
  </div>
  <div class="w3-third" >
	<?php echo $errormessage ?>
  </div>	
  </form>
<div class="w3-responsive" >
  <table class="w3-table w3-striped w3-small" style="width:100%">
    <tr>
      <th style="width:7%">Position</th>
      <th style="width:25%">Artist</th>
      <th style="width:30%">Title</th>
	   <th style="width:10%">Last Week</th>
	   <th style="width:10%">Weeks on Chart</th>
	   <th style="width:10%">Highest Position</th>
    </tr>
	 
   <?php
    if (($_SERVER["REQUEST_METHOD"] == "POST") ) {
    if ($reply[1]['http_reply']['http_code'] != 200) {
//			echo  'aaa'   ;
			echo'<tr> No jobs matching supplied criteria</tr>';
		} else {
			foreach ($reply[0] as $job) {


				echo "<tr margin='none'>
					   <td> {$job['position']} </td>
					   <td> <a href=chart_artist_direct.php?artist=".urlencode($job['artist']).">{$job['artist']} </a></td>
					   <td> {$job['song']} </td>
					   <td> {$job['previous_week']} </td>
					   <td> {$job['weeks_on_chart']} </td>
					   <td> {$job['highest']} </td>
					   		   
					   
					 </tr>";
			};
		};
    }
	
?>

</div></div>
</table>
</body>
</html>