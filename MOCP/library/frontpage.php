
<html>

<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/templates/heading.inc.php' ?>
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/functions.inc.php';?>





<div class="w3-sidebar w3-bar-block mocpMenu" style="width:20%">
<?php include $_SERVER['DOCUMENT_ROOT'] . '/MOCP/library/left_menu.inc.php' ?>
</div>

<div style="margin-left:25%">
<form <form class="w3-container">
<div class="w3-container w3-center "> <h2><?php echo 'Job Monitor';?></h2> </div>

</form>
<div>
<?php //echo "Gabba Gabba hey " . $_SESSION["token"];?>
</div>
<div id="tableholder"></div> 
<script>

   $(document).ready(function(){
    refreshTable();
    });

function refreshTable(){
   setInterval(function(){  
    $('#tableholder').load('get_schedule_data.php?v=1')
   }, 1000);
 }

</script>
</div>
</body>

</html>