<?php

$update = htmlspecialchars($_GET["update"]);
$system = '';
$suite = '';
$job = '';

$errormessage = '';
$errors = false;
$initial_load = true;
?>
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php'; ?>

<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
  <?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/left_menu.inc.php' ?>
</div>

<div style="margin-left:20%">
  <?php


  if ($_SERVER["REQUEST_METHOD"] == "POST") {

    if (empty($_POST['sys'])) {
      $errormessage = 'All values must be supplied';
      $_SESSION['last_system'] = '';
    } else {
      $system = $_POST['sys'];
      $_SESSION['last_system'] = $_POST['sys'];
    }
    if (empty($_POST['suite'])) {
      $errormessage = 'All values must be supplied';
      $_SESSION['last_suite'] = '';
    } else {
      $suite = $_POST['suite'];
      $_SESSION['last_suite'] = $_POST['suite'];
    }
    if (empty($_POST['job'])) {
      $job = 0;
      $_SESSION['last_job'] = 0;
    } else {
      $job = $_POST['job'];
      $_SESSION['last_job'] = $_POST['job'];
    }
    if ($errormessage == '') {
      $payload = "{ \"system\" : \"{$system}\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\"}";
      $response = run_web_service('job', $payload, 'GET');
      $reply = json_decode($response, true);
      // echo $reply[1]['http_reply']['http_code'] == 200;
      if ($reply[1]['http_reply']['http_code'] == 200) {
        header(sprintf('Location: /MOCP/library/update_job.php?system=%s&suite=%s&job=%d', $system, $suite, $job));
        ob_flush();
        exit;
      } elseif ($reply[1]['http_reply']['http_code'] == 404) {
        $errormessage = 'Job does not exist';
      } else {
        $errormessage = 'Unable to retrieve job';
      }
    }
  };


  /* 	$payload = "{ \"system\" : \"{$system }\", \"suite\" : \"{$suite}\",	\"job\" : \"{$job}\"}";
	$response = run_web_service('job', $payload, 'GET');
	$reply=json_decode($response,true);
 */

  $repost = htmlspecialchars($_SERVER["PHP_SELF"]) . sprintf('?update=%s', $update);
  ?>

  <form <form class="w3-container" method="post" action="<?php echo $repost; ?>">
    <table>
      <tr>
        <div class="w3-container w3-center ">
          <h2><?php echo 'Update ' . ucwords($update); ?></h2>
        </div>
        <div class="w3-row-padding">
          <div class="w3-third" style="width:10%">
            <?php system_select(); ?>
          </div>
          <div class="w3-third" style="width:10%">
            <?php suite_select(); ?>
          </div>
          <div class="w3-third" style="width:10%">
            <input type="number" class="w3-input " maxlength="6" id="job" name="job" value=<?php echo $_SESSION['last_job'] ?> placeholder="JOB">
          </div>

          <div class="w3-third" style="width:10%">
            <input class="w3-button w3-light-grey w3-round-large w3-medium" type="submit" value="Get Job">
          </div>
      </tr>
      <tr style='color:red;font-weight:bold'>
        <span>
          <?php echo $errormessage ?>
</div>
</tr class="w3-third">
</span>
</form>

</table>
</body>

</html>