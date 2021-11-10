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

    </tr>
<?php
	$payload = "{\"schedule_date\" : \"{$_SESSION['schedule_date']}\"}";
	$reply=get_schedule_jobs($payload);
	if (array_key_exists('system_message', $reply)) {
		echo $reply['system_message'];
	} else {
		foreach ($reply as $job) {
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
				 </tr>";
		};
	};

?>
  </table>