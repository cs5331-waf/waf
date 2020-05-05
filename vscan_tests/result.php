<!DOCTYPE html>
<html>
<body>

<h1>Voting Result</h1>

<?php
if(isset($_GET['id']) && !empty($_GET['id'])){
	if(isset($_GET['candidate']) && !empty($_GET['candidate'])){
		echo "<h1>Thank you for voting!</h1>";
		if($_GET['candidate'] == 'white') {
			echo "<p> You have voted for Mr.White.</p>";
		} else if($_GET['candidate'] == 'green') {
			echo "<p> You have voted for Mrs.Green.</p>";
		}
		else {
			echo "<h1>Invalid Candidate!</h1>";
			echo "<p> Please vote for either Mr.White or Mrs.Green!</p>";
		}
		
	} else {
		echo "<h1>Invalid Candidate!</h1>";
		echo "<p> Please vote for either Mr.White or Mrs.Green!</p>";
	}
    
} else {
    echo "<p>Invalid Election Id</p>";
}
?>

</body>
</html>