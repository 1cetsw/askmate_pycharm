<html>
<body>
<?php
/* Get the name of the uploaded file */
$filename = $_FILE['file']['name'];
$location = "upload/".$filename;
if( move_uploaded_file($_FILES['file']['tmp_name'],$location))(
echo '<p>file uploaded successfully</p>';)
else(echo '<b> Error uploading file.</b>;'
)
?>
</body>
</html>