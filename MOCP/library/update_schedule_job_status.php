<?php 
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>





<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/left_menu.inc.php' ?>
</div>

<div style="margin-left:25%">

<div>

</div>
<div>
<?php 
$system='CRED';
$suite='DAY';
$job='';
$schedule_date=$_SESSION['schedule_date'];
$status='RQ';
$date_validate="(?:19|20)\[0-9\]{2}-(?:(?:0\[1-9\]|1\[0-2\])-(?:0\[1-9\]|1\[0-9\]|2\[0-9\])|(?:(?!02)(?:0\[1-9\]|1\[0-2\])-(?:30))|(?:(?:0\[13578\]|1\[02\])-31))" ;
$errormessage='';
$errors=false;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if ((empty($_POST['sys'])) or 
	  (empty($_POST['suite'])) or
	  (empty($_POST['job'])) or
	  (empty($_POST['schedule_date'])) or
	  (empty($_POST['status']))) {
		$errormessage="All fields must be supplied!";
		$errors = true;
	} else {
		$system = strtoupper(($_POST["sys"]));
		$suite = strtoupper(($_POST["suite"]));
		$job = ($_POST["job"]);
		$schedule_date = ($_POST["schedule_date"]);
		$status = strtoupper(($_POST["status"]));
    } 

    if (! $errors ) {
		$errormessage = "Status updated";
        $payload = "{ \"system\" : \"{$system }\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\",\"schedule_date\" : \"{$schedule_date}\",\"new_status\" : \"{$status}\"}";
        $response = run_web_service('schedule_job', $payload, 'PUT');
	    $reply=json_decode($response,true);
	
 
		if ($reply[1]['http_reply']['http_code'] == 200) {
			$errormessage = "Status updated";
		} else {	
			$errormessage = 'Updated failed or status already set';
		} 
	}
}
?>
<div class="w3-container w3-center "> <h2><?php echo 'Update Scedule Job Status';?></h2> </div>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
  <table class="w3-table  w3-border w3-container w3-center w3-left-align w3-small" style="width:50%">
    <tr>    
	</tr>
	<tr>
		<td><label>System</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="system" name="sys" value="<?php echo $system?>"></td>
	</tr>	
	<tr>
		<td><label>Suite</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10" id="suite" name="suite" value="<?php echo $suite?>"></td>
	</tr>
	<tr>
		<td><label>Job</label></td>
		<td><input type="number" class="w3-input " maxlength="6" id="job" name="job" value="<?php echo $job?>"></td>
	</tr>
		<tr>
		<td><label>Schedule Date</label></td>
<!--		<td><input type="text" class="w3-input " pattern="<?php echo $date_validate ?>" title = 'Date in YYYY-MM-DD format' maxlength="6" id="schedule_date" name="schedule_date" value="<?php echo $schedule_date?>"></td>-->
		<td><input type="text" class="w3-input " maxlength="6" id="schedule_date" name="schedule_date" value="<?php echo $schedule_date?>"></td>

	</tr>
	<tr>
		<td><label>New Status</label></td>
		<td><input type="text"class="w3-input " style="text-transform:uppercase" maxlength="2" id="status" name="status" value="<?php echo $status?>"></td>
	</tr>
	<tr><td  colspan="2" style="color:red;font-weight:bold"> <?php echo $errormessage?></td></tr>
  </table>
    <br><input class="w3-button w3-white w3-round-large w3-medium" type="submit" value="Submit">
</form>
</div> 
</div>
</body>

</html>