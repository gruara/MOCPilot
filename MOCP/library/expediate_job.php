
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
$system='';
$suite='';
$job='';
$schedule_date=$_SESSION['schedule_date'];
$status='RQ';
$date_validate="(?:19|20)\[0-9\]{2}-(?:(?:0\[1-9\]|1\[0-2\])-(?:0\[1-9\]|1\[0-9\]|2\[0-9\])|(?:(?!02)(?:0\[1-9\]|1\[0-2\])-(?:30))|(?:(?:0\[13578\]|1\[02\])-31))" ;
$errormessage='';
$errors=false;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	if (empty($_POST['sys'])) {
		$errormessage = 'All values must be supplied';
		$_SESSION['last_system'] = '';
	} else {
		$system = $_POST['sys'];
		$_SESSION['last_system'] = $_POST['sys'];
	}
	if (empty($_POST['suite'])) {
		$errormessage = 'All values must be supplied';
		$_SESSION['last_suite'] = '';
	} else {
		$suite = $_POST['suite'];
		$_SESSION['last_suite'] = $_POST['suite'];
	}
	if (empty($_POST['job'])) {
		$job = 0;
		$_SESSION['last_job'] = 0;
	} else {
		$job = $_POST['job'];
		$_SESSION['last_job'] = $_POST['job'];
	}
	if (empty($_POST['schedule_date'])) {
		$errormessage = 'All values must be supplied';
	} else {
		$schedule_date = $_POST['schedule_date'];
	}
	if (empty($_POST['yn'])) {
		$errormessage = 'All values must be supplied';

	} else {
		$override_dependencies = $_POST['yn'];
	}
    if ($errormessage == '') {
        if ($override_dependencies == 'YES') {
           $status='RQ';
        } else {
           $status='SQ';
        }
        $schedule_time=date("H:i:s");
        $payload = "{ \"system\" : \"{$system }\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\",\"schedule_date\" : \"{$schedule_date}\",\"status\" : \"{$status}\",\"schedule_time\" : \"{$schedule_time}\"}";
        $response = run_web_service('schedule_job', $payload, 'PUT');
	    $reply=json_decode($response,true);
	
 
		if ($reply[1]['http_reply']['http_code'] == 200) {
			$errormessage = "Job expediated";
		} else {	
			$errormessage = 'Updated failed';
		} 
	}
}
?>
<div class="w3-container w3-center "> <h2><?php echo 'Expediate Job';?></h2> </div>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
  <table class="w3-table  w3-border w3-container w3-center w3-left-align w3-small" style="width:50%">
    <tr>    
	</tr>
	<tr>
		<td ><label for "system"> Select System</label></td>
		<td class="mocpSelect"><?php system_select(); ?></td>
	</tr>	
	<tr>
		<td><label>Suite</label></td>
		<td><?php suite_select(); ?></td>
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
		<td><label>Override dependencies</label></td>
		<td><?php yes_no(); ?></td>
	</tr>
	<tr><td  colspan="2" style="color:red;font-weight:bold"> <?php echo $errormessage?></td></tr>
  </table>
    <br><input class="w3-button w3-light-grey w3-round-large w3-medium" type="submit" value="Submit">
</form>
</div> 
</div>
</body>

</html>