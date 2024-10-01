const picVal=document.getElementById("picVal");
const l_aVal=document.getElementById("l_aVal");
const ratingVal=document.getElementById("ratingVal");
const revVal=document.getElementById("revVal");
const ap=document.getElementById("AddPost");
const lp=document.getElementById("logging");
const sp=document.getElementById("signing");
const useVal=document.getElementById("useVal");
const passVal=document.getElementById("passVal");
const suseVal=document.getElementById("suseVal");
const spassVal1=document.getElementById("spassVal1");
const spassVal2=document.getElementById("spassVal2");
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
    lp.style.display="block";
    }
    function logDown(){
        lp.style.display="none";
        }
    function log_me_in(){
        const user=useVal.value;
        const password=passVal.value;
        logDown();
        //must be used for auth
    }
    function signme(){
        sp.style.display="block";
        }
        function signDown(){
            sp.style.display="none";
            }
        function sign_me_in(){
            const n_user=suseVal.value;
            const n_p_1=spassVal1.value;
            const n_p_2=spassVal2;
            signDown();
            //must be used for auth
        }