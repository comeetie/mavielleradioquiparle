#!/bin/node
var io=require('socket.io-client');
var socket= io.connect('http://localhost:3000');
socket.emit('playPlaylist', {'name':process.argv[2]});
socket.emit('getQueue');
socket.on('pushQueue',function(data)
{
    console.log(data.length);
    process.exit()
});
