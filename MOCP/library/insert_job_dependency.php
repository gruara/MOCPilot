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
$system='';
$suite='';
$job='';
$dep_system='';
$dep_suite='';
$dep_job='';
$met_if_not_scheduled='N';
$error1='';
$error2='';
$error3='';
$error4='';
$error5='';
$error6='';
$error7='';


$errormessage='';
$errors=false;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST['sys'])) {

		$error1="Field must be supplied!";
		$errors = true;
	} else {
		$system = strtoupper(($_POST["sys"]));

    } 
    if (empty($_POST['suite'])) {

		$error2="Field must be supplied!";
		$errors = true;
	} else {
		$suite = strtoupper(($_POST["suite"]));

    }
    if (empty($_POST['job'])) {

		$error3="Field must be supplied!";
		$errors = true;
	} else {
		$job = strtoupper(($_POST["job"]));

    }	
	if (empty($_POST['dep_sys'])) {

		$error4="Field must be supplied!";
		$errors = true;
	} else {
		$dep_system = strtoupper(($_POST["dep_sys"]));

    } 
    if (empty($_POST['dep_suite'])) {

		$error5="Field must be supplied!";
		$errors = true;
	} else {
		$dep_suite = strtoupper(($_POST["dep_suite"]));

    }
    if (empty($_POST['dep_job'])) {

		$error6="Field must be supplied!";
		$errors = true;
	} else {
		$dep_job = strtoupper(($_POST["dep_job"]));

    }	
    if (empty($_POST['met_if_not_scheduled'])) {

		$error4="Field must be supplied!";
		$errors = true;
	} else {
		$met_if_not_scheduled = ($_POST["met_if_not_scheduled"]);

    }
 
    if (! $errors ) {
		$errormessage = "Status updated";
        $payload = "[{ \"system\" : \"{$system }\",
					  \"suite\" : \"{$suite}\",
					  \"job\" : \"{$job}\",
					  \"dep_system\" : \"{$dep_system }\",
					  \"dep_suite\" : \"{$dep_suite}\",
					  \"dep_job\" : \"{$dep_job}\",
					  \"met_if_not_scheduled\" : \"{$met_if_not_scheduled}\"
					  }]";
        $response = run_web_service('job_dependency',$payload, 'POST');
	    $reply=json_decode($response,true);
	
 // TODO Standardise response handling from web services

		if ($reply[1]['http_reply']['http_code'] == 200) {
			$errormessage = "Job inserted";
		} else {	
			$errormessage = "Insert failed";
		} 
	}
}
?>
<div class="w3-container w3-center "> <h2><?php echo 'Insert Job Dependency';?></h2> </div>
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
  <table class="w3-table  w3-border w3-container w3-center w3-left-align w3-small" style="width:50%">
    <tr>    
	</tr>
	<tr>
		<td><label>System</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="system" name="sys" value="<?php echo $system?>"></td>
		<td><span class="error"> <?php echo $error1;?></span></td>
	</tr>	
	<tr>
		<td><label>Suite</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10" id="suite" name="suite" value="<?php echo $suite?>"></td>
		<td><span class="error"> <?php echo $error2;?></span></td>
	</tr>
	<tr>
		<td><label>Job</label></td>
		<td><input type="number" class="w3-input " maxlength="6" id="job" name="job" value="<?php echo $job?>"></td>
		<td><span class="error"> <?php echo $error3;?></span></td>
	</tr>
	<tr>
		<td><label>Dependent System</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="dep_system" name="dep_sys" value="<?php echo $dep_system?>"></td>
		<td><span class="error"> <?php echo $error4;?></span></td>
	</tr>	
	<tr>
		<td><label>Dependent Suite</label></td>
		<td><input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10" id="dep_suite" name="dep_suite" value="<?php echo $dep_suite?>"></td>
		<td><span class="error"> <?php echo $error5;?></span></td>
	</tr>
	<tr>
		<td><label>Dependent Job</label></td>
		<td><input type="number" class="w3-input " maxlength="6" id="dep_job" name="dep_job" value="<?php echo $dep_job?>"></td>
		<td><span class="error"> <?php echo $error6;?></span></td>
	</tr>
	<tr>
		<td><label>Met If Not Scheduled</label></td>
		<td><input type="text"  class="w3-input " maxlength="50"id="met_if_not_scheduled" name="met_if_not_scheduled" value="<?php echo $met_if_not_scheduled?>"></td>
		<td><span class="error"> <?php echo $error7;?></span></td>

	<tr><td  colspan="2" style="color:red;font-weight:bold"> <?php echo $errormessage?></td></tr>
  </table>
    <br><input class="w3-button w3-white w3-round-large w3-medium" type="submit" value="Submit">
</form>
</div> 
</div>
</body>

</html>