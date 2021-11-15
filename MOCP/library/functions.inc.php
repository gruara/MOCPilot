<?php

function run_web_service($service, $payload, $method) {
  $curl = curl_init();
  $url = 'http://192.168.68.133:80/api/v1.0/MOCPilot/' . $service;

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


?>