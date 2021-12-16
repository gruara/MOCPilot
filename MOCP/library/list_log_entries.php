<?php 

$system='';
$suite='';
$job='';
$schedule_date=$_SESSION['schedule_date'];

$errormessage='';
$errors=false;
$initial_load=true;
?>
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>

<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/left_menu.inc.php' ?>
</div>

<div style="margin-left:20%">
<?php 


if ($_SERVER["REQUEST_METHOD"] == "POST") {
	if (empty($_POST['sys'])) {
		$_SESSION['last_system']='';
	} else {
		$system=$_POST['sys']; 
		$_SESSION['last_system']=$_POST['sys']; 
	}
	if (empty($_POST['suite'])) {
	  $_SESSION['last_suite']='';
	} else {
	  $suite=$_POST['suite']; 
	  $_SESSION['last_suite']=$_POST['suite']; 
	}
	if ((empty($_POST['job']))  and ($_POST['job'] != 0))  {
	  $_SESSION['last_job']='';
	} else {
	  $job=$_POST['job']; 
	  $_SESSION['last_job']=$_POST['job']; 
	}  
	if (empty($_POST['schedule_date']))  {
	  $_SESSION['last_schedule_date']='';
	} else {
	  $schedule_date=$_POST['schedule_date']; 
	  $_SESSION['last_schedule_date']=$_POST['schedule_date'];   
	}
	if ( $errormessage == '') {
	
		$payload = "{ \"system\" : \"{$system }\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\", \"schedule_date\" : \"{$schedule_date}\"}";
		$response = run_web_service('log', $payload, 'GET');
		$reply=json_decode($response,true);

	};
};
?>
<form <form class="w3-container" method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
<div class="w3-container w3-center "> <h2><?php echo 'List Log Entries';?></h2> </div>
<div class="w3-row-padding">
  <div class="w3-third" style="width:10%" >
  <?php system_select($all=true); ?>
  </div>
  <div class="w3-third" style="width:10%">
  <?php suite_select($all=true); ?>
  </div>
  <div class="w3-third" style="width:10%">
	<input type="number"  class="w3-input " maxlength="6"id="job" name="job" value="<?php echo $_SESSION['last_job']?>" placeholder="JOB" >
 </div> 
   <div class="w3-third" style="width:15%">
   <input type="text" class="w3-input " maxlength="10" id="schedule_date" name="schedule_date" value="<?php echo  $_SESSION['last_schedule_date']?>" placeholder="SCHEDULE DATE">
 </div>


  <div class="w3-third" style="width:10%" >
	<input class="w3-button w3-light-grey w3-round-large w3-medium"  type="submit" value="List">
  </div>
  <div class="w3-third" >
	<?php echo $errormessage ?>
  </div>	
</div>
</form>
<div>

</div>
<div class="w3-responsive" >
  <table class="w3-table w3-striped w3-small" style="width:100%">
    <tr>
	  <th>Timestamp</th>	
      <th>System</th>
      <th>Suite</th>
      <th>Job</th>
	  <th>Action</th>
	  <th>Schedule Date</th>
	  <th>Status</th>

<?php
    if (($_SERVER["REQUEST_METHOD"] == "POST") ) {
	
 // TODO Standardise response handling from web services
 if ($reply[1]['http_reply']['http_code'] != 200) {
			echo'<tr> No jobs matching supplied criteria</tr>';
		} else {
			foreach ($reply[0] as $job) {


				echo "<tr margin='none'>
					   <td> {$job['timestamp']} </td>	
					   <td> {$job['system']} </td>
					   <td> {$job['suite']} </td>
					   <td> {$job['job']} </td>
					   <td> {$job['action']} </td>
					   <td> {$job['schedule_date']} </td>
					   <td> {$job['status']} </td>
					   
					   
					   
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