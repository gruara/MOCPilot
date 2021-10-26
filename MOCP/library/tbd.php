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
<form <form class="w3-container">

<div class="w3-row-padding">
  <div class="w3-third" style="width:10%">
    <input class="w3-input w3-border" type="text" placeholder="System" >
  </div>
  <div class="w3-third" style="width:10%">
    <input class="w3-input w3-border" type="text" placeholder="Suite" >
  </div>
  <div class="w3-third" style="width:10%">
    <input class="w3-input w3-border" type="text" placeholder="Job" >
  </div>
  <div class="w3-third" style="width:15%">
    <input class="w3-input w3-border" type="text" placeholder=<?php  echo $_SESSION['schedule_date'] ?>>
  </div>
  <div class="w3-third" style="width:10%">
	<input class="w3-button w3-white w3-round-large w3-small" type="submit" value="Refresh">
  </div>
</div>
</form>
<div>
<?php //echo "Gabba Gabba hey " . $_SESSION["token"];?>
</div>
To be defined
</div>
</body>

</html>