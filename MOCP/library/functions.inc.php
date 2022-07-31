<?php


function run_web_service($service, $payload, $method) {
  $curl = curl_init();
  $url = 'http://pi4-1:80/api/v1.0/MOCPilot/' . $service;

  curl_setopt_array($curl, array(
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_ENCODING => '',
    CURLOPT_MAXREDIRS => 10,
    CURLOPT_TIMEOUT => 0,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
    CURLOPT_CUSTOMREQUEST => $method,
    CURLOPT_POSTFIELDS => $payload,
  
  
    CURLOPT_HTTPHEADER => array(
      'user: ' . $_SESSION['user_id'],
      'token: ' . $_SESSION['token'],
      'Content-Type: application/json'
    ),
  ));
  
  $response = curl_exec($curl);
  
  curl_close($curl);
  return $response;
}



function get_schedule_date() {
  $payload='{}';
  $response=run_web_service('schedule_date', $payload, 'GET');
  $reply=json_decode($response,true);
  if ($reply[1]['http_reply']['http_code'] == 200) {
    return $reply[0]['schedule_date']; 
  } else {
    return 'Not defined';
  };
}

function system_select($all=false) {
  
  $systems=array("CRED","MOCP","PI","SYSTEM");
  
  echo '<select class="w3-select"  name="sys",id="system">';
  echo '<option value="" disabled>System</option>';
  if ($all) {
    echo "<option value=''> All </option>";

  }
  foreach ($systems as $sysname) {
          if ($sysname == $_SESSION["last_system"]) {
            $selected='selected';
          } else {
            $selected='';
          }
          echo "<option value=$sysname $selected> $sysname </option>";
  };
  echo "</select>";

}

function suite_select($all=false) {
  $suites=array("ADHOC", "DAY", "MOCP", "TP", "WEEK");
  echo '<select class="w3-select"  name="suite",id="suite">';
  echo  '<option value="" disabled>Suite</option>';
  if ($all) {
    echo "<option value=''> All </option>";

  }
  foreach ($suites as $suitename) {
    if ($suitename == $_SESSION["last_suite"]) {
      $selected='selected';
    } else {
      $selected='';
    }
    echo "<option value=$suitename $selected> $suitename </option>";
};
    echo "</select>";

}

function status_select() {
  echo '<select class="w3-select"  name="status",id="status">
          <option value="" disabled selected>Status</option>
          <option value="RF"> RF </option>
          <option value="RQ"> RQ </option>
          <option value="SQ"> SQ </option>
       </select>';

}

function dep_system_select() {
  echo '<select class="w3-select"  name="dep_sys",id="dep_system">
          <option value="" disabled selected>System</option>
          <option value="CRED"> CRED </option>
          <option value="PI"> PI </option>
          <option value="SYSTEM"> SYSTEM </option>
        </select>';

}

function dep_suite_select() {
  echo '<select class="w3-select"  name="dep_suite",id="dep_suite">
        <option value="" disabled selected>Suite</option>
          <option value="ADHOC"> ADHOC </option>
          <option value="DAY"> DAY </option>
          <option value="TP"> TP </option>
          <option value="WEEK"> WEEK </option>
      </select>';

}

function yes_no() {
  echo '<select class="w3-select"  name="yn",id="yn">
       
          <option value="YES" > YES </option>
          <option value="NO"> NO </option>

      </select>';

}