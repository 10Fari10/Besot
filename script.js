const picVal=document.getElementById("picVal");
const l_aVal=document.getElementById("l_aVal");
const ratingVal=document.getElementById("ratingVal");
const revVal=document.getElementById("revVal");
const ap=document.getElementById("AddPost");
function popUp(){
ap.style.display="block";
}
function popDown(){
    ap.style.display="none";
    }
function submission(){
    const pic=picVal.value;
    const l_a=l_aVal.value;
    const rate=ratingVal.value;
    const rev=revVal.value;
    popDown();
    //must take these value and generate a post with them
}
function logme(){
    ap.style.display="block";
    }
    function logDown(){
        ap.style.display="none";
        }
    function log_me_in(){
        const pic=picVal.value;
        const l_a=l_aVal.value;
        const rate=ratingVal.value;
        const rev=revVal.value;
        logDown();
        //must take these value and generate a post with them
    }
    function signme(){
        ap.style.display="block";
        }
        function signDown(){
            ap.style.display="none";
            }
        function sign_me_in(){
            const pic=picVal.value;
            const l_a=l_aVal.value;
            const rate=ratingVal.value;
            const rev=revVal.value;
            signDown();
            //must take these value and generate a post with them
        }