<?php 
session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
if ( !isset( $_SESSION['user_id'])) {
  header('Location: /MOCP/library/signon.php');
  ob_flush();
}
?>
<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">

<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" type="text/css" href="/MOCP/themes/styles.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

<style>

</style>

</head>

<body lang=EN-GB >

<div class="w3-container w3-margin">

<table  border=0 cellspacing=0 cellpadding=0 width=100%

<tr >
  <td width=100% valign=middle >
  <h1>MOC <?php print $_SESSION["suite"];?></h1>
  <h2>Where Miserable Old Cnuts come to die</h2>
  </td>
 </tr>
</table>
</div>