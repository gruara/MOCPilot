<?php 
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>

  <?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>

  <table class="w3-table w3-striped w3-border w3-small" style="width:70%">
    <tr>

      <th>System</th>
      <th>Suite</th>
      <th>Job</th>
	  <th>Status</th>
	  <th style="width:25%">Schedule<br>Time</th>	

    </tr>
<?php
	$payload = "{\"schedule_date\" : \"{$_SESSION['schedule_date']}\"}";
	$response=run_web_service('schedule_job', $payload, 'GET');
	$reply=json_decode($response,true);

	if ($reply[1]['http_reply']['http_code'] == 200) {
		foreach ($reply[0] as $job) {
			if ($job['status'] == 'RS') {
				$color = "style='color:orange;font-weight:bold'"; }
			elseif ($job['status'] == 'RE') {
				$color = "style='color:red;font-weight:bold'"; }
			else {
				$color = "style='color:black;font-weight:normal'";
			};
			echo "<tr {$color}'>
						
						<td> {$job['system']} </td>
						<td> {$job['suite']} </td>
						<td> {$job['job']} </td>
						<td> {$job['status']} </td>
						<td> {$job['schedule_time']} </td>
					</tr>";
					
			};
		
	} else {
		echo 'No Schedule Data Available';
	};

	

?>
  </table>