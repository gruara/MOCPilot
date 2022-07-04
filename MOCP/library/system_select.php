<html>
<?php 
session_start();
$_SESSION["suite"]='Systems'; 
?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>
<div><table class="w3-table" style="width:90%">
<tr>
<td></td>
<td style="width:30%"><h1>MOC Pilot </h1></td>
<td class="w3-panel w3-padding-16"><a href="/MOCP/library/frontpage.php"><button class="w3-button w3-white w3-border w3-border-red w3-round-large">Go</button></a></td>
</tr>

<tr>
<td></td>
<td style="width:30%"><h1>MOC Charts </h1></td>
<td class="w3-panel w3-padding-16"><a href="/MOCP/library/charts.php"><button class="w3-button w3-white w3-border w3-border-red w3-round-large">Go</button></a></td>
</tr>

</table></div>


</html>