
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>





<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/left_menu.inc.php' ?>
</div>

<div style="margin-left:25%">

<div>
<div class="w3-container w3-center "> <h2><?php echo 'System Information';?></h2> </div>
</div>
<div>
  <table class="w3-table w3-striped w3-border" style="width:90%">
    <tr>


    </tr>
<?php
	$payload='{}';
	$response=run_web_service('sysinfo',$payload,'GET');
	$reply=json_decode($response,true);
	if ($reply[1]['http_reply']['http_code'] != 200) {
		echo $reply['system_message'];
	} else {
		echo '<tr><td>Schedule Date</td><td>' . $reply[0]['schedule_date'] . '</td></tr>';
		echo '<tr><td>Apache Web Services</td><td>' . $reply[0]['apache'] . '</td></tr>';
		echo '<tr><td>Job Schedular</td><td>' . $reply[0]['schedular'] . '</td></tr>';
		echo '<tr><td>Job Controller</td><td>' . $reply[0]['job_controller'] . '</td></tr>';
		echo '<tr><td>Job Runner</td><td>' . $reply[0]['job_runner'] . '</td></tr>';
	};
?>



  </table>

</div> 
</div>
</body>

</html>