<?php
function check_credentials($payload) {


$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.68.133:80/api/v1.0/MOCPilot/user',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'GET',
  CURLOPT_POSTFIELDS => $payload,


  CURLOPT_HTTPHEADER => array(
    'Content-Type: application/json'
  ),
));

$response = curl_exec($curl);

curl_close($curl);
return $response;


}
function get_schedule_date() {


$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.68.133:80/api/v1.0/MOCPilot/schedule_date',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'GET',
));

$response = curl_exec($curl);


$reply=json_decode($response,true);
if (curl_getinfo($curl, CURLINFO_HTTP_CODE) == 200) {
	return $reply[0]['payload']['schedule_date'];
}
else {
	return 'Not defined';
}
curl_close($curl);	
}

function get_schedule_jobs($payload) {

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.68.133:80/api/v1.0/MOCPilot/schedule_job',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'GET',
  CURLOPT_POSTFIELDS => $payload,
  CURLOPT_HTTPHEADER => array(
    'user: ' . $_SESSION['user_id'],
	'token: ' . $_SESSION['token'],
    'Content-Type: application/json'
  ),
));

$response = curl_exec($curl);


//echo $response;
$reply=json_decode($response,true);
if (curl_getinfo($curl, CURLINFO_HTTP_CODE) == 200) {
	return $reply[0];
	
}
else {
	return $reply['http_reply']  ;
}	
curl_close($curl);
}


function get_system_info() {


$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.68.133:80/api/v1.0/MOCPilot/sysinfo',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'GET',
  CURLOPT_HTTPHEADER => array(
    'user: ' . $_SESSION['user_id'],
	'token: ' . $_SESSION['token'],
   ),
));

$response = curl_exec($curl);
$reply=json_decode($response,true);
if (curl_getinfo($curl, CURLINFO_HTTP_CODE) == 200) {
	return $reply[0];
	
}
else {
	return $reply['http_reply'] ;
}	
curl_close($curl);


}
function update_schedule_job_status ($payload) {

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://192.168.68.133:80/api/v1.0/MOCPilot/schedule_job',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'PUT',
  CURLOPT_POSTFIELDS => $payload,
  CURLOPT_HTTPHEADER => array(
    'user: ' . $_SESSION['user_id'],
	'token: ' . $_SESSION['token'],
	'Content-Type: application/json'
  ),
));

$response = curl_exec($curl);

return $response;

curl_close($curl);

	
	
	
}	
?>