<?php 
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$system=htmlspecialchars($_GET["system"]);
$suite=htmlspecialchars($_GET["suite"]);
$job=htmlspecialchars($_GET["job"]);
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

$payload = "{ \"system\" : \"{$system }\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\"}";
$response = run_web_service('job', $payload, 'GET');
$reply=json_decode($response,true);
$response=$reply[0][0];
$description=$response['description'];
$run_on=$response['run_on'];
$or_run_on=$response['or_run_on'];
$or_run_on2=$response['or_run_on2'];
$but_not_on=$response['but_not_on'];
$and_not_on=$response['and_not_on'];
$schedule_time=$response['schedule_time'];
$command_line=$response['command_line'];
$last_scheduled=$response['last_scheduled'];
$error1='';
$error2='';
$error3='';
$error4='';
$error5='';
$error6='';
$error7='';
$error8='';
$error9='';
$error10='';
$error11='';
$error12='';

$errormessage='';
$errors=false;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
 
    if (empty($_POST['description'])) {

		$error4="Field must be supplied!";
		$errors = true;
	} else {
		$description = ($_POST["description"]);

    }
    if (empty($_POST['run_on'])) {

		$error5="Field must be supplied!";
		$errors = true;
	} else {
		$run_on = strtoupper(($_POST["run_on"]));

    }
    if (empty($_POST['schedule_time'])) {

		$error10="Field must be supplied!";
		$errors = true;
	} else {
		$schedule_time = strtoupper(($_POST["schedule_time"]));

    }
	if (empty($_POST['command_line'])) {

		$error11="Field must be supplied!";
		$errors = true;
	} else {
		$command_line = ($_POST["command_line"]);

    }
	if (empty($_POST['last_scheduled'])) {

		$error12="Field must be supplied!";
		$errors = true;
	} else {
		$last_scheduled = ($_POST["last_scheduled"]);

    }
    if (! $errors ) {
		$errormessage = "Status updated";
        $payload = "{ \"system\" : \"{$system }\",
					  \"suite\" : \"{$suite}\",
					  \"job\" : \"{$job}\",
					  \"description\" : \"{$description}\",
					  \"run_on\" : \"{$run_on}\",
					  \"or_run_on\" : \"{$or_run_on}\",
					  \"or_run_on2\" : \"{$or_run_on2}\",
					  \"but_not_on\" : \"{$but_not_on}\",
					  \"and_not_on\" : \"{$and_not_on}\",
					  \"schedule_time\" : \"{$schedule_time}\",
					  \"command_line\" : \"{$command_line}\",
					  \"last_scheduled\" : \"{$last_scheduled}\"
					  }";
        $response = run_web_service('job', $payload, 'PUT');
	    $reply=json_decode($response,true);
	
 // TODO Standardise response handling from web services

		if ($reply[1]['http_reply']['http_code'] == 200) {
			$errormessage = "Job updated";
		} else {	
			$errormessage = "Update failed";
		} 
	}
}
$repost=htmlspecialchars($_SERVER["PHP_SELF"]).sprintf('?system=%s&suite=%s&job=%d',$system,$suite,$job);
?>
<div class="w3-container w3-center "> <h2><?php echo 'Update Job';?></h2> </div>
<form method="post" action="<?php echo $repost;?>">
  <table class="w3-table  w3-border w3-container w3-center w3-left-align w3-small" style="width:50%">
    <tr>    
	</tr>
	<tr>
		<td><label>System</label></td>
		<td><label><?php echo $system; ?></label></td>
		<td><span class="error"> <?php echo $error1;?></span></td>
	</tr>	
	<tr>
		<td><label>Suite</label></td>
        <td><label><?php echo $suite; ?></label></td>
		<td><span class="error"> <?php echo $error2;?></span></td>
	</tr>
	<tr>
		<td><label>Job</label></td>
        <td><label><?php echo $job; ?></label></td>
    	<td><span class="error"> <?php echo $error3;?></span></td>
	</tr>

	<tr>
		<td><label>Description</label></td>
		<td><input type="text"  class="w3-input " maxlength="50"id="system" name="description" value="<?php echo $description?>"></td>
		<td><span class="error"> <?php echo $error4;?></span></td>
	</tr>		<tr>
		<td><label>Run On</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="run_on" name="run_on" value="<?php echo $run_on?>"></td>
		<td><span class="error"> <?php echo $error5;?></span></td>
	</tr>		<tr>
		<td><label>Or Run On</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="or_run_on" name="or_run_on" value="<?php echo $or_run_on?>"></td>
		<td><span class="error"> <?php echo $error6;?></span></td>
	</tr>		<tr>
		<td><label>Or Run On</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="or_run_on2" name="or_run_on2" value="<?php echo $or_run_on2?>"></td>
		<td><span class="error"> <?php echo $error7;?></span></td>	
	</tr>	<tr>
		<td><label>But Not On</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="but_not_on" name="but_not_on" value="<?php echo $but_not_on?>"></td>
		<td><span class="error"> <?php echo $error8;?></span></td>
	</tr>		<tr>
		<td><label>And Not On</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="and_not_on" name="and_not_on" value="<?php echo $and_not_on?>"></td>
		<td><span class="error"> <?php echo $error9;?></span></td>
	</tr>		<tr>
		<td><label>Schedule Time</label></td>
		<td><input type="text"  class="w3-input " maxlength="10" id="schedule_time" name="schedule_time" value="<?php echo $schedule_time?>"></td>
		<td><span class="error"> <?php echo $error10;?></span></td>
	</tr>		
	<tr>
		<td><label>Command Line</label></td>
		<td><input type="text"  class="w3-input " maxlength="500"id="command_line" name="command_line" value="<?php echo $command_line?>"></td>
		<td><span class="error"> <?php echo $error11;?></span></td>
	</tr>
	<tr>
		<td><label>Last Scheduled</label></td>
		<td><input type="text"  class="w3-input " maxlength="500"id="last_scheduled" name="last_scheduled" value="<?php echo $last_scheduled?>"></td>
		<td><span class="error"> <?php echo $error12;?></span></td>
	</tr>	
	<tr><td  colspan="2" style="color:red;font-weight:bold"> <?php echo $errormessage?></td></tr>
  </table>
    <br><input class="w3-button w3-light-grey w3-round-large w3-medium" type="submit" value="Submit">
</form>
</div> 
</div>
</body>

</html>