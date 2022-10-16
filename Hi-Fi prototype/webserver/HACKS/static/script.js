/*
    Script Sheet
 */
var global_counters = []

$( document ).ready(function() {
    // Getting the values of the improvements
    getGlobalCounters();
});

function getGlobalCounters(){
    var server = window.location.href;
    var	http = new XMLHttpRequest();
    var txt = "", x;
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.responseText);
            for (x in response['counters']){
                global_counters.push(response['counters'][x].grammar.toString());
                global_counters.push(response['counters'][x].spelling.toString());
            }

            replaceCounters();
        }
    };
    http.open("GET", server + "/getCounters", true);
    http.send();
}

function replaceCounters(){
    var grammar = document.getElementById("grammar_counter");
    text = " words."
    if (Number(global_counters[0]) === 1 | Number(global_counters[1]) === 1){
        text = " word."
    }
    grammar.innerText = global_counters[0] + text;

    var spelling = document.getElementById("spelling_counter");
    spelling.innerText = global_counters[1]+ text;
}