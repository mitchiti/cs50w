document.addEventListener('DOMContentLoaded', function() {

  // // Use buttons to toggle between views
  // document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  // document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  // document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  // document.querySelector('#compose').addEventListener('click', compose_email);
  if (document.querySelector('#following-posts') != null){
      document.querySelector('#following-posts').addEventListener('click', () => load_posts(true, "", 1));
  }
  document.querySelector('#post-button').addEventListener('click', save_post);
  document.querySelector('#cancel-button').addEventListener('click', () => load_posts(false, "", 1));

  // By default, load all posts  (following = false)
  load_posts(false, "", 1);
});



function load_posts(following, user, page) {

  document.querySelector("#posts-view").innerHTML = '';

  document.querySelector('#post-view').style.display = 'block';
  document.querySelector('#edit-view').style.display = 'none';
  document.querySelector('#profile-view').style.display = 'none';


  if (document.querySelector('#following-posts') == null){
    const no_posts = document.createElement('h5')
    no_posts.innerText = 'Log in or register first'

    document.querySelector("#posts-view").append(no_posts);
    document.querySelector('#post-view').style.display = 'none';

    return
  }

  document.querySelector('#following-posts').style.fontWeight = "normal";
  document.querySelector('#all-posts').style.fontWeight = "bold";
  
  fetch_string = '/posts/'

  // Show the selected as bold
  if (following) {
    document.querySelector('#all-posts').style.fontWeight = "normal";
    document.querySelector('#following-posts').style.fontWeight = "bold";
    fetch_string = '/following/'
  } else if (user) {
    document.querySelector('#all-posts').style.fontWeight = "normal";
    document.querySelector('#following-posts').style.fontWeight = "normal";
    fetch_string = `/user_posts/${user}`
    document.querySelector('#post-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'block';
  }

  fetch(fetch_string + '?' + new URLSearchParams({
    page: page
  }))
  .then(response => response.json())
  .then(posts => {

      if (posts.posts.length == 0){
        const no_posts = document.createElement('h5')
        no_posts.innerText = 'No Posts'

        document.querySelector("#posts-view").append(no_posts);
      }

      // Display the paginator
      if (posts.num_pages > 1) {
        const pag_nav = document.createElement('nav')
        const pag_ul = document.createElement('ul')
        pag_ul.className = 'pagination'
        pag_nav.appendChild(pag_ul)

        const prev_nav = document.createElement('li')
        if (page > 1){
          prev_nav.className = 'page-item'
          prev_nav.addEventListener('click', () => {
            load_posts(following, user, page - 1)
        })
        } else {
          prev_nav.className = 'page-item disabled'
        }
        prev_nav.innerHTML = `<a class="page-link" href="#">Previous</a>`
        pag_ul.appendChild(prev_nav)
      
      for (let i = 1; i <= posts.num_pages; i++) {
        const index_nav = document.createElement('li')
        index_nav.innerHTML = `<a class="page-link" href="#">${i}</a>`
        if (i == page){
          index_nav.className = 'page-item active'
        } else {
          index_nav.className = 'page-item'
        }
        index_nav.addEventListener('click', () => {
          load_posts(following, user, i)
        })        
        pag_ul.appendChild(index_nav)
      }

      const next_nav = document.createElement('li')
      next_nav.innerHTML = `<a class="page-link" href="#">Next</a>`
      if (page < posts.num_pages){
        next_nav.className = 'page-item'
        next_nav.addEventListener('click', () => {
            load_posts(following, user, page + 1)
        })
       } else {
        next_nav.className = 'page-item disabled'
       }
       pag_ul.appendChild(next_nav)



        document.querySelector("#posts-view").append(pag_nav);
      }


      //  Add cards for all the posts on this page
      posts.posts.forEach(post => {

      const card = document.createElement('div');
      card.className = 'card border-secondary mb-3';

      let title = document.createElement('button');
      title.className = 'card-header btn'
      title.innerHTML = post.poster;
      title.className = 'card-header';  
      title.addEventListener('click', () => show_user(post.poster));
      card.appendChild(title);

      const cardBody = document.createElement('div');
      cardBody.className = 'card-body';
      cardBody.innerText = post.text
      card.appendChild(cardBody);

      const date = document.createElement('div');
      date.innerText = post.timestamp
      card.appendChild(date);
      
      if (post.editable){
        let span_field = document.createElement('span')
        span_field.className = 'float-right'
        let edit_field = document.createElement('button');
        edit_field.className = 'btn btn-link'
        edit_field.innerText = "Edit"
        edit_field.addEventListener('click', () => edit_post(post));
        span_field.appendChild(edit_field)
        card.appendChild(span_field);
      } else {
        const likes = document.createElement('btn');
        likesclassName = 'btn btn-link'
        let likers = JSON.parse(post.likers).length
        let user_likes = false;
        if (post.user_likes){
          user_likes = true;
        }
        likes.innerText = `\u2764  ${likers}`
        likes.addEventListener('click', async () => {
          user_likes = !user_likes;
          await fetch(`like/${post.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                "like": user_likes
            })
          })
          if (user_likes){
            likers = likers + 1;
          } else {
            likers = likers - 1;
          }
          likes.innerText = `\u2764  ${likers}`
        })
        // likes.addEventListener('mouseover', () {

        // })
        card.appendChild(likes);
      }

      document.querySelector("#posts-view").append(card);
    });

});
}

function save_post() {

  console.log("saving");
  fetch('/post/', {
    method: 'POST',
    body: JSON.stringify({
        text: document.querySelector('#post-text').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

}

function show_user(user) {

  document.querySelector("#profile-view").innerHTML = '';

  const card = document.createElement('div');
  card.className = 'text-center mx-auto';
  // card.style = 'width: 18rem;'
  let title = document.createElement('button');
  title.className = 'card-header btn'
  title.innerHTML = user;
  title.className = 'card-header';  
  card.appendChild(title);

  const cardBody = document.createElement('div');
  cardBody.className = 'card-body';
  const img = document.createElement('img');
  img.src = 'static/network/user.png';
  cardBody.appendChild(img);

  fetch(`/user/${user}`)
  .then(response => response.json())
  .then(aUser => {
    const following = document.createElement('div');
    following_object = JSON.parse(aUser.following)
    following.innerHTML = `Following: ${following_object.length}`
    cardBody.appendChild(following);

    const followers = document.createElement('div');
    followers_object = JSON.parse(aUser.followers)
    followers.innerHTML = `Followers: ${followers_object.length}`
    cardBody.appendChild(followers);

    if (!aUser.current){
      const userFollowing = document.createElement('btn');
      if (aUser.userfollowing){
        userFollowing.className = 'btn btn-default'
        userFollowing.innerHTML = 'Unfollow';
        followString = false
      } else {
        userFollowing.className = 'btn btn-primary'
        userFollowing.innerHTML = 'Follow';
        followString = true
      }
      userFollowing.addEventListener('click', async () => {
        await fetch(`follow/${aUser.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              "follow": followString
          })
        })
        if (followString){
          userFollowing.className = 'btn btn-default'
          userFollowing.innerHTML = 'Unfollow';
          followString = false
        } else {
          userFollowing.className = 'btn btn-primary'
          userFollowing.innerHTML = 'Follow';
          followString = true
        }
  
      });
      cardBody.appendChild(userFollowing);
    }
  })
  

  card.appendChild(cardBody);




  document.querySelector("#profile-view").append(card);

  load_posts(false, user);
}

function edit_post(post) {
  console.log(post)
  document.querySelector('#post-view').style.display = 'none';
  document.querySelector('#edit-view').style.display = 'block';
  document.querySelector('#profile-view').style.display = 'none';

  document.querySelector("#posts-view").innerHTML = '';

  document.querySelector("#edit-text").innerText = post.text;

  document.querySelector('#edit-button').addEventListener('click', () => {
    console.log("saving");
    fetch('/post/', {
      method: 'POST',
      body: JSON.stringify({
          id: post.id,
          text: document.querySelector('#edit-text').value,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });  
  });

}
