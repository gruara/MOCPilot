<html>
<?php 
   session_start();
   $_SESSION["suite"]='Charts'; 
?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>

<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/charts_left_menu.inc.php' ?>
</div>

<div style="margin-left:25%">
<form <form class="w3-container">
<div class="w3-container w3-center "> <h2>Random Chart</h2> </div>

<?php
      $chart_id = rand(1, 3501);
      $payload = "{ \"chart_id\" : \"$chart_id\" }";
		$response = run_web_service('chart', $payload, 'GET');
		$reply=json_decode($response,true);
?>

<div class="w3-responsive" >
  <table class="w3-table w3-striped w3-small" style="width:100%">
    <tr>
      <th style="width:7%">Position</th>
      <th style="width:25%">Artist</th>
      <th style="width:30%">Title</th>
	   <th style="width:10%">Last Week</th>
	   <th style="width:10%">Weeks on Chart</th>
	   <th style="width:10%">Highest Position</th>
    </tr>
	 
   <?php
    if ($reply[1]['http_reply']['http_code'] != 200) {
//			echo  'aaa'   ;
			echo'<tr> No jobs matching supplied criteria</tr>';
		} else {
			foreach ($reply[0] as $job) {


				echo "<tr margin='none'>
					   <td> {$job['position']} </td>
					   <td> {$job['artist']} </td>
					   <td> {$job['song']} </td>
					   <td> {$job['previous_week']} </td>
					   <td> {$job['weeks_on_chart']} </td>
					   <td> {$job['highest']} </td>
					   		   
					   
					 </tr>";
			};
		};
      $payload = "{ \"chart_id\" : \"$chart_id\" }";
		$response = run_web_service('chart_date', $payload, 'GET');
		$reply=json_decode($response,true);
      $det=$reply[0][0];
      echo "<tr><th>
            <td> {$det['date_from']} </td>
            </th></tr>"
	
?>


</html>