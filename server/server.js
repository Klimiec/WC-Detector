

var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs')


var app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Map of monitoring places
var toilets = {}
toilets['wc1'] = 'Free';
toilets['wc2'] = 'Free';
toilets['urinal'] = 'Free';


app.get('/toilets', function(req, res) {
  console.log("# /toilets")
 // res.header('Content-Type', 'application/json');
  res.header("Access-Control-Allow-Origin", "*");
  //res.header("Access-Control-Allow-Methods", "GET");
  res.json(toilets);
});

// Id = name of the place
// 
app.get('/toilet/:id', function(req, res) {
  if(req.params.id in toilets) {
 	  var toilet = toilets[req.params.id];
 	  console.log("# /toilet/:id Get the data for " + toilet);
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


app.put('/:id/:state', function(req, res) {
  toilets[req.params.id] = req.params.state;
  console.log("# /:id/:state : " + toilets[req.params.id])
  res.json(true);
});


app.listen(process.env.PORT || 8181);
