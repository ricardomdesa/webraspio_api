
$(document).ready(function(){
    console.log('app.js running');

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {

        var tempo = parseInt(msg.tempo);
        var secrest = parseInt(msg.cont);

        if(tempo > 0){
            numbers_string = '<p>' + 'Tempo restante para desligar: ' + tempo.toString() + ' minuto(s)' + '</p>';
        }
        else{
            numbers_string = '<p>' + 'Tempo restante para desligar: ' + secrest.toString() + ' segundo(s)' + '</p>';
        }
        
        $('#log').html(numbers_string);

        if(msg.cont == 0){
            console.log("atualiza pag")
            window.location.href = 'http://' + document.domain + ':' + location.port + '/';
        }
    });

     //receive details from server
     socket.on('intervalo', function(msg) {
        console.log("atualiza pag 1 inter")
        var t_on = parseInt(msg.t_on);
        var t_off = parseInt(msg.t_off);
        var repetir = parseInt(msg.repetir);

        numbers_string2 = '<p>' + 'T_on '+ t_on.toString() +' , T_off '+ t_off.toString() +' e repeticao intervalo: ' + repetir.toString() + ' vezes </p>';
        
        $('#log_i').html(numbers_string2);

        if(msg.stsInter == false){
            console.log("atualiza pag")
            window.location.href = 'http://' + document.domain + ':' + location.port + '/';
        }

    });

});