
  //popDown fuction-click the 'x' for the post form to dissappear
  document.getElementById("closePop").addEventListener("click", popDown);
  function popDown(){
  document.getElementById("addPost").style.display="none";
  }
//opens profile pic form
  document.getElementById("user_pfp").addEventListener("click", pfp_up);
  function pfp_up(){
  document.getElementById("user_form").style.display="block";
  }
//closes profile pic form
  document.getElementById("close_user_pfp").addEventListener("click", pfp_down);
  function pfp_down(){
  document.getElementById("user_form").style.display="none";
  }


//submission for profile pic form
  document.getElementById('user_pfp').addEventListener('submit', pfp_submission);
  async function pfp_submission(event) {
    event.preventDefault(); 
    const pfp = document.getElementById("pfp_Val").value;
    if(pfp==''){
        alert("Please choose a file.");
    }
    else{
    const data_to_send = {
        Profile: pfp,           
        parent:-1,
    };
    try {
        const response = await fetch('pfp_post', {
            method: 'POST',
            headers: {
                //We can make profile madatory png or jpg or make it flexible up to you
                'Content-Type': 'image/png',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: data_to_send
        });

        if (response.ok) {
            sent_data = await response.json();
            console.log("OK!:", sent_data);
            //function might be needed here
            document.getElementById("picVal").value = '';
            
            pfp_down();  
        }
        else{
            alert("Failed to insert image.");
            pfp_down();
        }
    } catch (error) {
        console.error("ERROR:", error);
        alert("An error occurred while submitting your profile image.");
    }
}
}
//function to actually load the pfp needs to be written

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
                        //Placeholder values
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
            sent_data = await response.json();
            fetchPinsAndReviews(); 
            console.log("OK!:", sent_data);

            //document.getElementById("picVal").value = '';
            document.getElementById("latVal").value = '';
            document.getElementById("longVal").value = '';
            document.getElementById("revVal").value = '';
            popDown();  
        }
        else{
            alert("Failed to create post.");
            popDown();
        }
    
    
    } catch (error) {
        console.error("ERROR:", error);
        alert("An error occurred while submitting your review.");
    }
}
}

  
  function pasteReviews(lat, long) {
    fetch(`/send_post/?lat=${lat}&long=${long}`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("ERROR!");
        }
        return response.json(); 
    })
    .then(data => {
        displayReviews(data); 
    })
   
}

function displayReviews(allPosts) {
    const dynamiccontainer = document.getElementById("revcontainer");
    dynamiccontainer.innerHTML = ""; 

    if (allPosts.length === 0) {
        const nomessage = document.createElement("p")
        nomessage.textContent = "No reviews available."
        dynamiccontainer.appendChild(nomessage)
        return;
    }

    for (let i in allPosts) {
        const post = allPosts[i];
        const postElement = document.createElement("div");
        postElement.classList.add("pinform");

        const Elem_pfp=document.createElement("div");
        Elem_pfp.classList.add("pfp");
        postElement.appendChild(Elem_pfp);

        const Elem_user = document.createElement("p");
        Elem_user.textContent = `Reviewed by : ${post.username}`;
        postElement.appendChild(Elem_user);

        const Elem_body = document.createElement("p");
        Elem_body.textContent = post.body;
        postElement.appendChild(Elem_body);

        const Elem_likes = document.createElement("span");
        Elem_likes.textContent = `Likes: ${post.likes}`;
        postElement.appendChild(Elem_likes);

        const likeButton = document.createElement("button")
        likeButton.textContent = "Like"
        likeButton.classList.add("likeBtn")
        likeButton.onclick = () => {
            likesincrement(post.id, Elem_likes)
        };
        postElement.appendChild(likeButton);

        dynamiccontainer.appendChild(postElement);
    }
}


  function likesincrement(postId, likesElement){

    fetch('/like/', {
        method : "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN 
        },
        body: JSON.stringify({ id: postId })
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
  
