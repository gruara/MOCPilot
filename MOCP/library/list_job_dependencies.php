<?php 
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
  


	$errormessage = "";
	$payload = "{ \"system\" : \"{$system }\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\"}";
	$response = run_web_service('job', $payload, 'GET');
	$reply=json_decode($response,true);


};

?>
<form <form class="w3-container" method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
<div class="w3-container w3-center "> <h2><?php echo 'List Job Dependencies';?></h2> </div>
<div class="w3-row-padding">
  <div class="w3-third" style="width:10%">
  	<?php system_select($all=true); ?>
  </div>
  <div class="w3-third" style="width:10%">
 	 <?php suite_select($all=true); ?>
  </div>
  <div class="w3-third" style="width:10%">
	<input type="text" style="text-transform:uppercase" class="w3-input " maxlength="10"id="job" name="job" value="<?php echo $job?>" placeholder="JOB" >
 </div>

  <div class="w3-third" style="width:10%">
	<input class="w3-button w3-light-grey w3-round-large w3-medium" type="submit" value="List">
  </div>
  <div class="w3-third" >
	<?php echo $errormessage ?>
  </div>	
</div>
</form>
<div>

</div>
<div class="w3-responsive">
  <table class="w3-table w3-striped w3-small" style="width:100%">
    <tr>
      <th>System</th>
      <th>Suite</th>
      <th>Job</th>
	  <th>Description</th>
	  <th>Dependent On</th>
	  <th>Met if not<br> sceduled?</th>
	  <th>File Dependency</th>
	  <th>Rule</th>
	</tr>

<?php
    if (($_SERVER["REQUEST_METHOD"] == "POST") ) {
	
 // TODO Standardise response handling from web services
 if ($reply[1]['http_reply']['http_code'] != 200) {
			$reply[1]['system_message'];
		} else {
			foreach ($reply[0] as $job) {


				echo "<tr>
					   <td> {$job['system']} </td>
					   <td> {$job['suite']} </td>
					   <td> {$job['job']} </td>
					   <td> {$job['description']} </td>
					   <td></td><td></td><td></td><td></td>
					   
					 </tr>";
				$payload = "{ \"system\" : \"{$job['system'] }\", \"suite\" : \"{$job['suite']}\",	\"job\" : \"{$job['job']}\"}";

				$response = run_web_service('job_dependency', $payload, 'GET');
				$reply2=json_decode($response,true);
				if ($reply[1]['http_reply']['http_code'] != 200) {
					$reply2[1]['system_message'];
				} else {
//					$jobx = 'bbb';
					foreach ($reply2[0] as $job2) {
					$jobx=sprintf( "%s %s %s", $job2['dep_system'], $job2['dep_suite'], $job2['dep_job']);
						echo "<tr><td></td><td></td><td></td><td></td>
								<td> {$jobx}</td>
								<td> {$job2['met_if_not_scheduled']}</td>
								<td></td><td></td>
							</tr>";
					};
				};
				$response = run_web_service('file_dependency', $payload, 'GET');
				$reply2=json_decode($response,true);

				if ($reply[1]['http_reply']['http_code'] != 200) {
					$reply2[1]['system_message'];
				} else {

					foreach ($reply2[0] as $job2) {

						echo "<tr><td></td><td></td><td></td><td></td><td></td><td></td>
								<td> {$job2['full_path']}</td>
								<td> {$job2['rule']}</td>
							</tr>";
					};				
			
				};
			};
		};
		$initial_load=false;
	};
?>
</div></div>
</table>
</body>

</html>