$(document).ready( () => {
    console.log("What's up, you cool baby?")
    let answer = setNewRiddle();

    $('#next-riddle').click(() => { 
        answer = setNewRiddle();
        return false; 
    });
    $("#reveal").click(() => {
        $("#answer-box").text(answer);
        $("#answer-box").transition('tada');
        return false;
    });

});

function setNewRiddle(){
    let rObj = getRandomRiddle();
    let riddle = rObj.riddle;
    let answer = rObj.answer;

    $("#riddle-box").text(riddle);
    $("#answer-box").text('');
    return answer;
}

function randomIndex(){
    const index = Math.floor(Math.random() * RIDDLES.length) + 1;
    return index;
}

function getRandomRiddle(){
    return RIDDLES[randomIndex()];
}