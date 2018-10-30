var express = require("express");
var app = express();

const bodyParser = require("body-parser");
const mysql		 = require("mysql");

/** bodyParser.urlencoded(options)
 *  * Parses the text as URL encoded data (which is how browsers tend to send form data from regular forms set to POST)
 *   * and exposes the resulting object (containing the keys and values) on req.body
 *    */
app.use(bodyParser.urlencoded({
	    extended: true
}));

app.get("/api/url", (req, res, next) => {
	 res.json(["Tony","Lisa","Michael","Ginger","Food"]);
});

app.get("/api/webcount", (req, res, next) => {
	connection = connectToDB();
	connection.query('SELECT count FROM webcount', function(error, results, fields)
		{
			if(error)
				throw error;
			res.json({"count": results[0].count});
			connection.query('update webcount set `count`='+(results[0].count+1) + ';');
		});
});

app.post("/api/bmi", function (req,res)  {
 
  const body = req.body.name
  res.set('Content-Type', 'text/plain')
  var height = parseFloat(req.body.height, 10);
  var weight = parseFloat(req.body.weight, 10);
  var name = req.body.name;
  var date = req.body.currentDate;
  var result = weight / (height*height);
  var connection = connectToDB();
	console.log(name);
	console.log(date);
  connection.query('INSERT INTO bmi (name, date, height, weight) VALUES ( "'+ name + '" , "'+date+'" , '+height+' , '+weight+ ' );', function(error, results, fields)
	{
		if(error)
		  throw error;
		res.send(result.toString());
	});
});

function connectToDB()
{
	var connection = mysql.createConnection({
		    host     : 'localhost',
		    database : 'gsd',
		    user     : 'hs',
		    password : 'hsfulda',
	});
	connection.connect(function(err) {
		    if (err) {
				        console.error('Error connecting: ' + err.stack);
				        return;
				    }

	});
	return connection;
}

app.get("/api/mysql", (req, res, next) => {
	var connection = connectToDB();
	connection.query('SELECT * FROM bmi', function (error, results, fields) 
	{
		if (error)
		    throw error;

	    results.forEach(result => {
			console.log(result);
		});
	});

	connection.end();
});

var PORT = 8080
app.listen(PORT, () => {
	 console.log("Server running on port " + PORT);
});
