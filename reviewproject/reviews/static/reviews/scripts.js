//popUP function-once clicking the post button the post form will popup
document.getElementById("postButton").addEventListener("click", popUp);
function popUp(){
document.getElementById("addPost").style.display="block";   
}
//popDown fuction-click the 'x' for the post form to dissappear
document.getElementById("closePop").addEventListener("click", popUp);
function popDown(){
document.getElementById("addPost").style.display="none";
}
//submission function-once form is completed with all fields entered with a value (not empty else different alert will appear)
//once check field are filled will empty values and automatically close
function submission(){
    const pic=document.getElementById("picVal").value;
    const l_a=document.getElementById("l_aVal").value;
    const rev=document.getElementById("revVal").value; 
     if(pic==''){
        alert("Please upload a png/jpg/jpeg.");
    }
    if(l_a==''){
        alert("Please enter a location/adress.");
    }
    if(rev==''){
        alert("Please enter a review.");
    }
    picVal.value='';
    l_aVal.value='';
    revVal.value='';
    popDown();  
}
//logme function- when Log-in button is click the log in form will appear
document.getElementById("lButton").addEventListener("click",logme);
function logme(){
document.getElementById("logging").style.display="block";
}
//logdown function- when 'x' is clicked log-in form will dissappear
document.getElementById("closeLog").addEventListener("click",logDown);
function logDown(){
    document.getElementById("logging").style.display="none";
}
//log_me_in fuction-once user clicks log in button field are checked the both are filled (or alerts appear) then values are
//cleared and form disappear
function log_me_in(){
    const user=document.getElementById("useVal").value;
    const password=document.getElementById("passVal").value;
    if(user==''){
        alert("Please enter a username.");
        }
    if(password==''){
        alert("Please enter a password.");
    }
    user.value='';
    password.value='';
    logDown();
}
//signme function- sign up form appear when clicking Sign-up button
document.getElementById("sButton").addEventListener("click",signme);
function signme(){
    document.getElementById("signing").style.display="block";
 }
//signDown function- when 'x' is sign up form is click the form disappears
document.getElementById("closeSign").addEventListener("click",signDown);
function signDown(){
    document.getElementById("signing").style.display="none";
 }
//sign_me_in function- when sign up button is clicked checks if all input are filled & password match otherwise alerts appear
//fields are cleared and form closes
function sign_me_in(){
    const n_user=document.getElementById("suseVal").value;
    const n_p_1=document.getElementById("spassVal1").value;
    const n_p_2=document.getElementById("spassVal2").value;
    if(n_user==''){
        alert("Please enter a username.");
    }
    if(n_p_1==''){
        alert("Please enter a password.");
    }
    if(n_p_2==''){
        alert("Please re-type password.");
    }
    if(n_p_1!=n_p_2 && (n_p_1!='')&&(n_p_2!='')){
        alert("Password don't match please try again!");
    }
    n_user.value='';
    n_p_1.value='';
    n_p_2.value='';
    signDown();
}