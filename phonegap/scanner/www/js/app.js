var resultDiv;

document.addEventListener("deviceready", init, false);
function init() {
	document.querySelector("#startScan").addEventListener("touchend", startScan, false);
	resultDiv = document.querySelector("#results");
}

function startScan() {
	console.log("inside function");
	/* $.getJSON('/_add_numbers', {
          a: $('input[name="a"]').val(),
          b: $('input[name="b"]').val()
        }, function(data) {
          $("#result").text(data.result);
        });*/
	$.getJSON('http://c00156721.pythonanywhere.com/',
				{
						text:"dummy"
				},
					function(data) 
					{
						$("#result_s").text(data.suc);
						
					}
				);
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
						
					}
				);
			
			}		 
    
		},
		function (error) {
			alert("Scanning failed: " + error);
		}
	);

}