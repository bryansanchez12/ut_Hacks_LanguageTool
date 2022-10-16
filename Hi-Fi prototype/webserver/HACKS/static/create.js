var textbox = document.getElementById('textbox')
var prev_words = 1
var marker = 0
var current_text = ""
var improved_txt = ""

jQuery(textbox).on('input', function() {
    text = textbox.value
    var temp = text.split(" ")
    var words = temp.length
    if (words > prev_words){
        current_text = text
        sendText(text);
    }
    prev_words = words
});

jQuery(textbox).click(function(){
    if (marker === 0 ){
        textbox.value = "";
        marker += 1;
    }
});

function sendText(text){
    var server = window.location.href
    var	http = new XMLHttpRequest();
    var param = 'text=' + text;
    http.open("POST", server + "/check", true);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200) {
            suggestions(http.responseText);
        }
    }
    http.send(param)
}

function checkDifference(wrong_text, improved_text){
    var words1 = wrong_text.split(" ");
    var words2 = improved_text.split(" ");
    var result = [];
    var i = 0;

    while(i < words1.length){
        if (words1[i] !== words2[i]){
            result.push(i);
        }
        i += 1
    }
    return result;
}

function suggestions(improved_text){
    // Finding the improved words
    var difference = checkDifference(current_text, improved_text);
    //Give the suggestion to the user
    var words1 = current_text.split(" ");
    var words2 = improved_text.split(" ");
    var num = 0;
    var html_suggestion = "";
    while (num < difference.length){
        var index = difference[num]
        html_suggestion += ""+
            "<tr id=\"row"+ num +"\">\n" +
            "    <td>Substitute <b>" + words2[index] + "</b> for <b>"+ words1[index] + "</b></td>\n" +
            "    <td id=\"btn"+ num +"\">\n" +
            "        <button type=\"button\" class=\"btn btn-primary\" onclick=\"doChange("+ index +", " + num +")\">\n" +
            "             Change</button>\n" +
            "    </td>\n" +
            "</tr>";
        num += 1;
    }
    document.getElementById('newSentences').innerHTML = html_suggestion;
    improved_txt = improved_text
}

function doChange(index, num){
    var words1 = textbox.value.split(" ")
    var words2 = improved_txt.split(" ")
    var result = ""
    i = 0;
    while (i < words1.length){
        if ( i === index){
            result += words2[i]
        }else{
            result += words1[i];
        }
        if (i < words1.length - 1){
          result += " "
        };
        i+=1;
    }
    textbox.value = result;
    new_button = ""+
        "    <td id=\"btn"+ index +"\">\n" +
        "        <button type=\"button\" class=\"btn btn-danger\" onclick=\"doUndo("+ index + ", " + num +")\">\n" +
        "             Undo</button>\n" +
        "    </td>\n";
    document.getElementById("btn" + num). innerHTML = new_button;
}

function doUndo(index, num){
    var words1 = textbox.value.split(" ")
    var words2 = current_text.split(" ")
    var result = ""
    i = 0;
    while (i < words1.length){
        if ( i === index){
            result += words2[i]
        }else{
            result += words1[i];
        }
        if (i < words1.length - 1){
            result += " "
        };
        i+=1;
    }
    textbox.value = result;
    document.getElementById("row" + num). innerHTML = "";
}

