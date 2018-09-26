const login = require ("facebook-chat-api");
const chalk = require ("chalk");
const fs = require ("fs");
const express = require ("express");

// SERVER & PAGE

var app = require('express')();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

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
		
		function chkMsg() {
			api.getThreadInfo("100005341296717", (err, ret) => {
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


sysLog("Starting C v4.8");

properLogin();

io.on('connection', function() {
	
	uCT(cumsg);
	uTI(cutim);
	uUT(cutho);
	
});