/*jslint undef: true */

const version = "4.9 (Jakdojade Edition)"
const threadID = "100005341296717"

const login =   require ("facebook-chat-api");
const chalk =   require ("chalk");
const fs =      require ("fs");
const express = require ("express");
const ngeocode = require ("node-geocoder");

const geocodeoptions = {
    provider: 'opencage',
    httpAdapter: 'https',
    apiKey:  '5103002a40c64aeeae57270fe17863df',
    formatter: null,
};

const geocoder = ngeocode(geocodeoptions);

// SERVER & PAGE

var app =       require('express')();
var server =    require('http').createServer(app);
var io =        require('socket.io')(server);

app.use(express.static(__dirname));

var cumsg;
var cutim;
var cutho;

if(process.env.PORT != undefined){
	server.listen(process.env.PORT);
	sysLog("Listening on port " + process.env.PORT);
}
else{
	server.listen(8080);
	sysLog("Listening on port 8080");
}

var dir = __dirname;

app.get('/', function(req, res) {
    res.sendFile(dir + '/index.html');
});

function getCoordsFromAddress(address, callback){
    let result;
    geocoder.geocode(address)
      .then(function(res) {
        var resultArr = res[0];
        var resultLat = resultArr['latitude'];
        var resultLon = resultArr['longitude'];
        console.log(res)
        sysLog(resultLat.toString());
        sysLog(resultLon.toString());
        result = resultLat.toString() + ":" + resultLon.toString();
        callback(result, resultLat, resultLon);
      })
      .catch(function(err) {
        sysErr(err);
      });
        sysLog(result);
    }



function uCT(newtext){
		var pagetext = newtext;
	    io.emit('change_text_ct', {
        pagetext: pagetext
    });
}

function uTI(newtext){
		var pagetext = newtext;
	    io.emit('change_text_ti', {
        pagetext: pagetext
    });
}

function uUT(newtext){
		var pagetext = newtext;
	    io.emit('change_text_ut', {
        pagetext: pagetext
    });
}

// END OF SERVER & PAGE

var lastcount = 0;
 
function sysLog(text) {
	console.log(chalk.red("SYS")+chalk.bold(" >> ")+chalk.gray(text)+chalk.gray("... ")+chalk.green.bold("OK"));
}

function sysErr(text) {
	console.log(chalk.red("SYS")+chalk.bold(" >> ")+chalk.gray(text)+chalk.gray("... ")+chalk.red.bold("ERROR"));
}

function untilThousand (amt) {
	return 1000-(amt - ((Math.floor(amt/1000))*1000));
}

function dateLog(date, amt){
	console.log(chalk.green("BOT")+chalk.bold(" >> ")+chalk.black.bgGreen(date)+chalk.bold(" > ")+chalk.black.bgGreen(amt)+chalk.bold(" < ")+chalk.black.bgGreen(untilThousand(amt)));
	
	cumsg = amt;
	cutho = untilThousand(amt);
	cutim = date;
	
	uTI(date);
	uCT(amt);
	uUT(untilThousand(amt));
}

function isNextMsgMilestone (amt) {
	if(untilThousand(amt) == 2) {
		sysLog("Milestone detected");
		return true;
	}
	else {
		return false;
	}
}
	
function getTime() {
	var myYear = new Date().getFullYear();
	var myDay = new Date().getDate();
	var myMonth = new Date().getMonth() + 1;
		if(myMonth.toString().length == 1) {
			myMonth = "0" + myMonth;
		}
	var myDate = myYear + "." + myMonth + "." + myDay;
	var myTime = new Date().toTimeString().replace(/.*(\d{2}:\d{2}:\d{2}).*/, "$1");
	var myDateTime = myDate + " " + myTime;
	return myDateTime;
}	

function properLogin () {
	login({appState: JSON.parse(fs.readFileSync('appstate.json', 'utf8'))}, (err, api) => {
		
		sysLog("Trying login with APPSTATE");
		
		api.setOptions({
			forceLogin: true
		});
        
        api.setOptions({selfListen: true})
        
        function jakdojade(addresses){
                let coor1;
                let coor2;
                let addressStart = addresses.split(",")[0];
                let addressEnd = addresses.substring(addresses.indexOf(",")+1);
                console.log("as " + addressStart);
                console.log("as " + addressEnd);
                getCoordsFromAddress(addressStart, function(result){
                coor1 = result;
                getCoordsFromAddress(addressEnd, function(result){
                coor2 = result;
                sysLog(coor1);
                sysLog(coor2);
                 api.sendMessage("[BOT] >> Jakdojade compiled.", threadID);
                 api.sendMessage("http://warszawa.jakdojade.pl/?fc=" + coor1 + "&tc=" + coor2 + "&t=2&as=true", threadID)
                }); 
                }); 
        }
        function cmdCheckMsg() {
            api.getThreadInfo(threadID, (err, ret) => {
                if(err) return sysErr("Getting messages");
                
                api.sendMessage("[BOT] >> Current message count: " + ret["messageCount"], threadID);
                sysLog(ret["messageCount"]);
                
                return ret["messageCount"];
            })
        }
        
        api.listen((err,message) => {
            if(message.threadID === threadID){
            if(message.body === ".version"){
                api.sendMessage("[BOT] >> This is C v" + version + " . The BOT is online.", threadID);
            }
            if(message.body === ".count"){
                cmdCheckMsg();
            }
            if(message.body.split(' ')[0] === ".coords"){
                console.log(message.body.substring(message.body.indexOf(" ")+1));
                getCoordsFromAddress(message.body.substring(message.body.indexOf(" ")+1), function(result){
                 api.sendMessage("[BOT] >> Retrieved coordinates: " + result, threadID);  
                });             
            }
                
            if(message.body.split(' ')[0] === ".jakdojade"){
                let coor1;
                let coor2;
                let addresses = message.body.substring(message.body.indexOf(" ")+1);
                let addressStart = addresses.split(",")[0];
                let addressEnd = addresses.substring(addresses.indexOf(",")+1);
                console.log("as " + addressStart);
                console.log("as " + addressEnd);
                getCoordsFromAddress(addressStart, function(result){
                coor1 = result;
                getCoordsFromAddress(addressEnd, function(result){
                coor2 = result;
                sysLog(coor1);
                sysLog(coor2);
                 api.sendMessage("[BOT] >> Jakdojade compiled.", threadID);
                 api.sendMessage("http://warszawa.jakdojade.pl/?fc=" + coor1 + "&tc=" + coor2 + "&t=2&as=true", threadID)
                }); 
                });     
            }
                
            if(message.body === ".wracam"){
                let addresses = "Walecznych 23 Warszawa,Reszelska 10 Warszawa";
                jakdojade(addresses);
            }
            if(message.body === ".jade"){
                let addresses = "Reszelska 10 Warszawa,Walecznych 23 Warszawa";
                jakdojade(addresses);
            }
            }
        });
        
		function chkMsg() {
			api.getThreadInfo(threadID, (err, ret) => {
				if(err) return sysErr("Getting messages");
				
				var currentcount = ret["messageCount"];
				
				if(lastcount < currentcount) {
					lastcount = currentcount;
					
					if(isNextMsgMilestone(currentcount)){
						api.sendMessage("[BOT] >> Nastepna wiadomość to > " + (currentcount+2) + "!", "100005341296717");
					}
					
					dateLog(getTime(), currentcount);
					return true;
				}
				
				else {
					return false;
				}
				
		})};
		
		setInterval(function() {
			chkMsg();
		}, 10);
		
	});
}


sysLog("Starting C v" + version);

properLogin();

io.on('connection', function() {
	
	uCT(cumsg);
	uTI(cutim);
	uUT(cutho);
	
});