function switch_entry(evt, entry) {
	var i, tabcontent, tablinks;

	// Hide elements
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i=0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}

	// Get elements and remove active
	tablinks = document.getElementsByClassName("tablinks");
	for (i=0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}
	
	// Shows current tab
	document.getElementById(entry).style.display = "block";
	evt.currentTarget.className += " active";
}
