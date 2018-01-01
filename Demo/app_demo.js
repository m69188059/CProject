var express = require('express');
var app = express();
var http = require('http');
var server = http.createServer(app);

//app.use(express.static('views'));
//app.use('/views', express.static('html'));
//app.use('/', express.static('json'));
app.use('/css', express.static('css'));
app.get('/', function(request, response){
    response.sendfile('demo.html');
    //app.use(express.static('views'));
});

server.listen(8080, function(){
  console.log('hello nodejs ');
}); 


var key;
var MongoClient = require('mongodb').MongoClient;
var mongo = require('mongodb').MongoClient;
MongoClient.connect("mongodb://localhost:27017/article_test", function (err, db) {
  if(err) throw err;
  mongo.connect("mongodb://localhost:27017/ptt3",function(err2,d){
  if(err2) throw err2;

  console.log('mongodb is running!');
  console.log('pttdb is running!');
  app.get('/process_get', function (req, res, next) {
    	response = {	Key:req.query.Key	};
    	key= req.query.Key;   
    	console.log(response);
	next();
   	},
  function (req, res, next){ //process_get
	console.log("next");
	res.sendfile("d3demo.html");
	app.get('/newsdb', function (resquest, response) {
		console.log('newsdb');
		var expr = '.*'+key+'.*';

		var query = { context : {$regex : expr }};
                var ptt_query = {Text : {$regex : expr}};

                var select = {_id:1,time:1,title:1,mood_score:1};
                var sel_ptt = {Link:1,time:1,mood_score:1,Title:1};
			
                var start_date = new Date(2012, 01, 01, 00, 00);
			
                var collection = db.collection('article_test');
                var ptt_col = d.collection('Gossiping');
                var ptt_col2 = d.collection('Gossiping2');
            

                collection.find(query,select).sort({'time':1}).toArray( function(err, result) {
		    if (err) throw err;
		    console.log("find ok"); 
	

                ptt_col.find(ptt_query,sel_ptt).toArray( function(err3,ptt_result) {
                    if (err3) throw err3;
                    console.log("Gossiping OK!!")

                    ptt_col2.find(ptt_query,sel_ptt).toArray( function(err4,ptt2_result){
                    if (err4) throw err4
                    console.log("Gossiping2 OK");

                    for(var i = 0 ; i<ptt2_result.length ; i++)
                        ptt_result.push(ptt2_result[i]);

                    for(var i=0 ; i<result.length ; i++)
                        ptt_result.push(result[i]);
//ptt_col2 //ptt_col //coll
                    response.send(ptt_result);   });  }); });

       //newsdb //function	
      })   ;});
//mongo //Mongoclient

}); });

