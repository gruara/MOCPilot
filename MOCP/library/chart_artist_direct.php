<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


?>
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>

<?php
$artist=$_GET['artist'];
$payload = "{ \"artist\" : \"{$artist }\"}";
$response = run_web_service('chart_artist', $payload, 'GET');
$reply=json_decode($response,true);
?>
<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/charts_left_menu.inc.php' ?>
</div>

<div style="margin-left:20%">

  <div class="w3-third" >

  </div>	

<div class="w3-responsive" >
  <table class="w3-table w3-striped w3-small" style="width:100%">
    <tr>
    <th style="width:20%" >Artist </th>
      <th style="width:30%" >Title</th>
	  <th style="width:10%" >First Entry</th>
	  <th style="width:10%" >Last Entry</th>
	  <th style="width:10%" >Weeks on Chart</th>
	  <th style="width:10%" >Highest</th>
    </tr>
<?php
foreach ($reply[0] as $job) {

    $payload = "{ \"artist\" : \"{$job['artist']}\",
                  \"song\" : \"{$job['song'] }\"}";

    $response = run_web_service('chart_song_summary', $payload, 'GET');

    $reply=json_decode($response,true);
                                                               
    $dets=$reply[0];
    
    echo "<tr margin='none'>
          
           <td> {$job['artist']} </td>
           <td> {$job['song']} </td>
           <td> {$dets[0]['earliest_date']} </td>
           <td> {$dets[0]['latest_date']} </td>
           <td> {$dets[0]['weeks_on_chart']} </td>
           <td> {$dets[0]['highest_position']} </td>
              
         </tr>";
};
?>
  </table>
</div>
</html>