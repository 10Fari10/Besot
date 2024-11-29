
  //popDown fuction-click the 'x' for the post form to dissappear
  document.getElementById("closePop").addEventListener("click", popDown);
  function popDown(){
  document.getElementById("addPost").style.display="none";
  }




  //submission function-once form is completed with all fields entered with a value (not empty else different alert will appear)
  //once check field are filled will empty values and automatically close

//
  document.getElementById('reviewForm').addEventListener('submit', submission);

  async function submission(event) {
    event.preventDefault();
    // const form = document.getElementById('reviewForm');
    const lat = document.getElementById("latVal").value;
    const long = document.getElementById("longVal").value;
    const review_text = document.getElementById("revVal").value;
    const img = document.getElementById("picVal");

    // if (img.files.length === 0) {
    //     alert("Please select a file.");
    //     return;
    // }
    if(review_text ==''){
        alert("Please enter review.")
    } else{
    const data_to_send = {
        latVal: lat,
        longVal: long,
        review: review_text,
        replies: 0,
        parent: -1,
    };
    const file = img.files[0];
    if (img.files.length !== 0){
    const reader = new FileReader();
    reader.onload = async function(e) {
        const bytes = e.target.result.split(',')[1]; // Base64 without metadata
        console.log(bytes);
        console.log(file.name);
        console.log("tead1");
        data_to_send.img = bytes;
        data_to_send.img_name = file.name;
        send(data_to_send);
    } 
    reader.readAsDataURL(file);
        }else{
        send(data_to_send);
    }
    }
    
}
async function send(data_to_send) {
    try {
        console.log("tbb")
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

        

        const Elem_user = document.createElement("p");
        Elem_user.textContent = `Reviewed by : ${post.username}`;
        postElement.appendChild(Elem_user);

        if("image" in post){
        const img_body = document.createElement("img");
        img_body.src = post.image;
        img_body.alt = "Review";
        postElement.appendChild(img_body);
        }

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

