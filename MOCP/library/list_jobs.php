<?php 
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$system='';
$suite='';
$job='';

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
		$system = '';
	} else {
		$system = strtoupper(($_POST["sys"]));
	};
  
	if (empty($_POST['suite'])) {
		$suite = '';
	} else {
		$suite = strtoupper(($_POST["suite"]));
	};
	$job = strtoupper(($_POST["job"]));

 	$errormessage = "";
	$payload = "{ \"system\" : \"{$system }\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\"}";
	$response = run_web_service('job', $payload, 'GET');
	$reply=json_decode($response,true);

};

?>
<form <form class="w3-container" method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
<div class="w3-container w3-center "> <h2><?php echo 'List Jobs';?></h2> </div>
<div class="w3-row-padding">
  <div class="w3-third" style="width:10%" >
  <?php system_select(); ?>
  </div>
  <div class="w3-third" style="width:10%">
  <?php suite_select(); ?>
  </div>
  <div class="w3-third" style="width:10%">
	<input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="job" name="job" value="<?php echo $job?>" placeholder="JOB" >
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
      <th>System</th>
      <th>Suite</th>
      <th>Job</th>
	  <th>Description</th>
	  <th>Run on</th>
	  <th>Or On</th>
	  <th>Or on</th>
	  <th>But not on</th>
	  <th>And not on</th>
	  <th>Schedule time</th>
	  <th>Command line</th>
	  <th>Last scheduled</th>
<?php
    if (($_SERVER["REQUEST_METHOD"] == "POST") ) {
	
 // TODO Standardise response handling from web services
 if ($reply[1]['http_reply']['http_code'] != 200) {
//			echo  'aaa'   ;
			$reply['system_message'];
		} else {
			foreach ($reply[0] as $job) {


				echo "<tr margin='none'>
					   <td> {$job['system']} </td>
					   <td> {$job['suite']} </td>
					   <td> {$job['job']} </td>
					   <td> {$job['description']} </td>
					   <td> {$job['run_on']} </td>
					   <td> {$job['or_run_on']} </td>
					   <td> {$job['or_run_on2']} </td>
					   <td> {$job['but_not_on']} </td>
					   <td> {$job['and_not_on']} </td>
					   <td> {$job['schedule_time']} </td>
					   <td> {$job['command_line']} </td>
					   <td> {$job['last_scheduled']} </td>
					   
					   
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