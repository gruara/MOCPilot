
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php'; ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>
<?php // include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/init.inc.php'; ?>
<div class="w3-sidebar w3-bar-block" style="width:25%">



</div>


<div style="margin-left:25%">
<div class="w3-container w3-margin mocpDiv">
<?php
// define variables and set to empty values
$unameErr = $passwordErr = "";
$uname = $password = "";
$errors = false;
$_SESSION["user_id"] = '';
$_SESSION["token"] = '';
$_SESSION["last_system"]='';
$_SESSION["last_suite"]='';
$_SESSION["last_job"]='';
$_SESSION["last_schedule_date"]='';
$_SESSION["last_schedule_time"]='';
$_SESSION["suite"]='Systems'; 


if ($_SERVER["REQUEST_METHOD"] == "POST") {
  if (empty($_POST["uname"])) {
    $unameErr = "User name is required";
	$errors = true;
  } else {
    $uname = ($_POST["uname"]);
  }

  if (empty($_POST["password"])) {
    $passwordErr = "Password is required";
	$errors = true;

  } else {
    $password = ($_POST["password"]);
  }
  if (! $errors ) {

	  $payload = "{ \"user_id\" : \"{$uname }\", \"password\" : \"{$password}\"}";
		

	  $response = run_web_service('user', $payload, 'GET');
	  $reply=json_decode($response,true);

 // TODO Standardise response handling from web services

	  if ($reply[1]['http_reply']['http_code'] == 200) {

			$_SESSION["user_id"] = $uname;
			$_SESSION["token"] = $reply[0]['token'];
			$_SESSION['schedule_date'] = get_schedule_date();
      
		  header('Location: /MOCP/library/system_select.php');
			ob_flush();
			exit;
	  }
	  $passwordErr = 'Sign on refused';

  }

	
}


	
?>

<form  method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
  <label for="fname">User name:</label><br>
  <input type="text" id="uname" name="uname"  value="<?php echo $uname?>"><span class="error"> <?php echo $unameErr;?></span><br>
  <label for="lname">Password:</label><br>
  <input type="password" id="password" name="password" > <span class="error"> <?php echo $passwordErr;?></span><br><br>
  <input class="w3-button w3-light-grey w3-round-large w3-medium" type="submit" value="Sign in">
</form>

</div>
</div>
</body>

</html>