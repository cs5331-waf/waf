<!DOCTYPE html>
<html>
<body>

<h1>Vote for your preferred candidate in this election</h1>

<?php
if(isset($_GET['id']) && !empty($_GET['id'])){
    echo "<p><a href='result.php?candidate=white&id=".$_GET['id']."'>Vote for Mr. White</a></p>";
	echo "<p><a href='result.php?candidate=green&id=".$_GET['id']."'>Vote for Mrs. Green</a></p>";
} else {
    echo "<p>No Election Id</p>";
}
?>

</body>
</html>
