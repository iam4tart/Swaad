

function Papas() {

	 $("#input_File").on("change", handleFile);
    // handleFile();

var renderCSVDropdown = function(csv) {
  var dropdown = $('#select_Style');
  var elements = csv.split(",");
  for (var i = 0; i < elements.length; i++) {
    var record = elements[i];
    var entry = $('<option>', {value: record, text: record})
    dropdown.append(entry);
  }
};

function handleFile() {
	// var rawFile = "file:///C:/Users/4TT4/Documents/drop/options.csv";
	// var file = new File(rawFile.responseText,"options.csv", {
	// 	type: "text/csv",
	//   });
    var file = $(this).prop('files')[0];

	console.log(file);
    var fileReader = new FileReader();
    fileReader.onload = function (evt) {
      renderCSVDropdown(evt.target.result);
    };
    fileReader.readAsText(file, "UTF-8");
}

};

function Populate() {


		Papas()
	};

