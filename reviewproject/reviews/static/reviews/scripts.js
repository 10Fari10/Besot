
  //popDown fuction-click the 'x' for the post form to dissappear
  document.getElementById("closePop").addEventListener("click", popDown);
  function popDown(){
  document.getElementById("addPost").style.display="none";
  }
  //submission function-once form is completed with all fields entered with a value (not empty else different alert will appear)
  //once check field are filled will empty values and automatically close

  
  document.getElementById('reviewForm').addEventListener('submit', submission);

  async function submission(event) {
    event.preventDefault(); 

    
    const lat = document.getElementById("latVal").value;
    const long = document.getElementById("longVal").value;
    const review_text = document.getElementById("revVal").value;
    
    if(review_text==''){
        alert("Please enter review.")
    }
    else{
    const data_to_send = {
        latVal: lat,           
        longVal: long,               //username and parent probably should be added here. not sure if replies should be a list
        review: review_text,        //replies is number of replies
        
        likes: 0,                   //Placeholder values
        replies: 0,
        parent:-1,
        
    };

    try {
        const response = await fetch('/map_post/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(data_to_send)
        });

        if (response.ok) {
            const sent_data = await response.json();
            console.log("OK!:", sent_data);

            //document.getElementById("picVal").value = '';
            document.getElementById("latVal").value = '';
            document.getElementById("longVal").value = '';
            document.getElementById("revVal").value = '';
            popDown();  
        } 
        pasteReviews(lat, long);
    
    } catch (error) {
        console.error("ERROR:", error);
    }
}
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
  function log_me_in(event){
      event.preventDefault();
      const user = document.getElementById("useVal");
      const password = document.getElementById("passVal");
      if(user.value == ''){
          alert("Please enter a username.");
      }
      if(password.value == ''){
          alert("Please enter a password.");
      }
      user.value = '';  
      password.value = '';  
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
  function sign_me_in(event){
      event.preventDefault();
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
  

  function pasteReviews(lat,long){

    fetch(`/send_post/?lat=${lat}&long=${long}`, {
        method: "GET",
        headers: {

            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
    })
  
    .then(response => {
        if(!response.ok){
            throw new error("ERROR!")
        }
        else{
            return response.json();
        }
    })
    .then(data => {
        displayReviews(data.allposts); 
    })
}
  

  function displayReviews(allPosts){
    const dynamiccontainer = document.getElementById("reviewcontainer");
    dynamiccontainer.innerHTML = "";

    for (let i = 0; i < allPosts.length; i++){
        const id = document.createElement("input");
        id.setAttribute("type", "hidden");
        id.setAttribute("name", "id");
        id.setAttribute("value", post.id);
        const post = allPosts[i];
        const postElement = document.createElement("div");
        postElement.classList.add("pinform");                           //i am using textcontent instead of innerhtml due to security risks 
        const Elem_user = document.createElement("p")
        Elem_user.textContent = post.username;
        postElement.appendChild(Elem_user);
        const Elem_body = document.createElement("p")              
        Elem_body.textContent = post.body;
        postElement.appendChild(Elem_body);
        const Elem_likes = document.createElement("span");
        Elem_likes.textContent = `Likes: ${post.likes}`;
        postElement.appendChild(Elem_likes)
        const likeButton = document.createElement("button");
        likeButton.textContent = "Like";
        likeButton.classList.add("likeBtn");
        likeButton.onclick = () => {
            likesincrement(post.id, likesElement);
        };
        postElement.appendChild(likeButton);
    }
    

  }


  function likesincrement(){

    fetch('/like/', {
        method : "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN 
        },
        body: JSON.stringify({ parent: post.parent })
    })

    .then(response => {
        if(!response.ok){
            throw new error("ERROR!")
        }
        else{
            return response.json();
        }
    })

    .then(data => {
        likesElement.textContent = `Likes: ${data.likes}`; 
    }) 
  }
  
