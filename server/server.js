

var express = require('express');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Map of monitoring places
var toilets = {}
toilets['wc1'] = 'Free';
toilets['wc2'] = 'Free';
toilets['urinal'] = 'Free';


app.get('/toilets', function(req, res) {
  res.json(toilets);
});

// Id = name of the place
app.get('/toilet/:id', function(req, res) {
  if(req.params.id in toilets) {
 	var toilet = toilets[req.params.id];
 	console.log("Get the data for " + toilet);
  	res.json(toilet);
  } else {
  	res.statusCode = 404;
    return res.send('Error 404: No toilet found');
  }
});

// Update state of cabins
app.put('/update', function(req, res) {
	if(!req.body.hasOwnProperty('id') || 
       !req.body.hasOwnProperty('state')) {
        res.statusCode = 400;
        console.log(req.body)
       return res.send('Error 400: Post syntax incorrect.');
  	} 
  toilets[req.body.id] = req.body.state
  console.log(toilets)
  res.json(true);
});


app.listen(process.env.PORT || 8181);
