const _like = document.getElementById('like');
var count = 0 ; // Number of likes fetched from database
if(_like){
    _like.addEventListener('click', e =>{
        if(count % 2 == 0){
            document.getElementById('like').style.color="#4267B2";
            count++;
            console.log(count);
        }else{
            document.getElementById('like').style.color="black";
            count--;
            console.log(count);
        }
    });
}

const _comment = document.getElementById('comment-btn');
if(_comment){
    _comment.addEventListener('click', e=>{
        document.getElementById('comment-input').style.display="block";
    });
}

// document.getElementById("like").addEventListener("click", function() {
//     console.log('pressed');
//   });