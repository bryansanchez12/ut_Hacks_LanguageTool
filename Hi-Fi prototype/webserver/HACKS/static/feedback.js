var scores = []
var previous_scores = []
var average_scores = []

$( document ).ready(function() {
    // Getting the values of the scores
    getGlobalScores();

});

/** Function that fetches the global scores in a JSON format
 *  And assign those values into the variable "global_scores"
 */
function getGlobalScores() {
    var server = window.location.href
    var	http = new XMLHttpRequest();
    var txt = "", x;
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            scoresJSON = JSON.parse(this.responseText);
            for (x in scoresJSON['scores']){
                scores.push(scoresJSON['scores'][x].score.toString())
                previous_scores.push(scoresJSON['scores'][x].prev_score.toString())
                average_scores.push(scoresJSON['scores'][x].avg_score.toString())
            }
            replaceAll()
        }
    };
    http.open("GET", server + "/getGlobalScores", true);
    http.send();
}

/** Function replace all the cards in the feedback by taking all the values
 *  from the variables "scores", "previous_scores" and "average_scores"
 */
function replaceAll(){
    replaceGlobalScores(scores[0], previous_scores[0], average_scores[0], "grammar");
    replaceGlobalScores(scores[1], previous_scores[1], average_scores[1], "spelling");
    replaceGlobalScores(scores[2], previous_scores[2], average_scores[2], "punctuation");
    replaceGlobalScores(scores[3], previous_scores[3], average_scores[3], "formality");
    replaceGlobalScores(scores[4], previous_scores[4], average_scores[4], "readability");
    replaceGlobalScores(scores[5], previous_scores[5], average_scores[5], "total");
}

/** Function that replace the default scores into the actual ones
 *  Requires:  x = Score
 *             y = Previous Score
 *             z = Average Score
 */
function replaceGlobalScores(x, y, z, cardName) {
    var cells = document.getElementById(cardName).getElementsByTagName("td");
    cells[0].innerText = x;
    cells[2].innerText = y;
    cells[4].innerText = z;
}