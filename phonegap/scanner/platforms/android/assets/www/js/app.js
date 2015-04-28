var resultDiv;

document.addEventListener("deviceready", init, false);
function init() {
	document.querySelector("#startScan").addEventListener("touchend", startScan, false);
	resultDiv = document.querySelector("#results");
}

function startScan() {

	cordova.plugins.barcodeScanner.scan(
		function (result) {
			var s = "Result: " + result.text + "<br/>" +
			"Format: " + result.format + "<br/>" +
			"Cancelled: " + result.cancelled;
			resultDiv.innerHTML = s;
			
			if(result.cancelled != true)
			{
				$.getJSON('http://c00156721.pythonanywhere.com/',
				{
						text:result.text.toString()
				},
					function(data) 
					{
						$("#result_s").text(data.suc);
						
					}//data function end
				);
			
			}//if end		 
		},
		function (error) {
			alert("Scanning failed: " + error);
		}
	);
}