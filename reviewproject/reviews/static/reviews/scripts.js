
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

//
  document.getElementById('reviewForm').addEventListener('submit', submission);

  async function submission(event) {
    event.preventDefault();
    // const form = document.getElementById('reviewForm');
    console.log("test1")
    const lat = document.getElementById("latVal").value;
    const long = document.getElementById("longVal").value;
    const review_text = document.getElementById("revVal").value;
    const img = document.getElementById("picVal");

    if (img.files.length === 0) {
        alert("Please select a file.");
        return;
    }

    const file = img.files[0];
    const reader = new FileReader();
    reader.onload = async function(e) {
        const bytes = e.target.result.split(',')[1]; // Base64 without metadata
        console.log(bytes);
        console.log(file.name);
        const data_to_send = {
            latVal: lat,
            longVal: long,
            review: review_text,
            replies: 0,
            parent: -1,
            img: bytes,
            img_name: file.name
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
                fetchPinsAndReviews();
                console.log("Post created:", sent_data);
                document.getElementById("latVal").value = '';
                document.getElementById("longVal").value = '';
                document.getElementById("revVal").value = '';
                popDown();
            } else {
                alert("Failed to create post.");
                popDown();
            }
        } catch (error) {
            console.error("ERROR:", error);
            alert("An error occurred while submitting your review.");
        }
    };
    reader.readAsDataURL(file);
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

        const img_body = document.createElement("img");
        img_body.src = post.image;
        img_body.alt = "Review";
        postElement.appendChild(img_body);

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
  
