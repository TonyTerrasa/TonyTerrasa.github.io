function displayanswer(question, value){ 
    var answer_id = "a" + question;
    var button_id = "b" + question;

    if(value == undefined){
        if (document.getElementById(answer_id).innerHTML.length == 0){
            value = 'show';
        }
        else {
            value = 'hide';
        }
    }
    console.log(value);
    // toggle off/on
    if(value == 'show'){
        document.getElementById(answer_id).innerHTML = answers[question-1];
        document.getElementById(button_id).innerHTML = 'Hide Answer';
    }
    else if(value == 'hide'){
        document.getElementById(answer_id).innerHTML = '';
        document.getElementById(button_id).innerHTML = 'Show Answer';
    }
    else {
        console.log("invalid value given for toggling: " + value);
    }
}

function toggleAll(){
    if(document.getElementById('toggle').innerHTML.includes('Show All')){
        document.getElementById('toggle').innerHTML = 'Hide All';
        value = 'show';
    }
    else{
        document.getElementById('toggle').innerHTML = 'Show All';
        value = 'hide';
    }

    // toggle all
    for(i = 1; i <= answers.length; i++){
        displayanswer(i, value);
    }
}

