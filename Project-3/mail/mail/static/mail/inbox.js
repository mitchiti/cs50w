document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#send').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

  console.log('DomContentloaded')
});



function send_email() {

  console.log("sending");
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function reply_email(email) {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Set composition fields
  document.querySelector('#compose-title').innerHTML = "Email Reply";
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.startsWith("Re")) {
    document.querySelector('#compose-subject').value = email.subject;
  } else {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#compose-body').innerHTML = `\n\n-----------------\nOn ${email.timestamp} ${email.sender} wrote:\n\n${email.body}`;
}


async function read_email(email) {

  if (!email.read){
    fetch(`emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  }

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#email-from').innerHTML = email.sender;
  document.querySelector('#email-to').innerHTML = email.recipients;
  document.querySelector('#email-subject').innerHTML = email.subject;
  document.querySelector('#email-timestamp').innerHTML = email.timestamp;
  document.querySelector('#email-body').innerHTML = email.body;
  document.querySelector('#reply').addEventListener('click', function() {
    reply_email(email);
  })

  // Archive
  const old_button = document.querySelector('#archive-button');
  if (old_button){
    document.querySelector('#email-view').removeChild(old_button)
  }

  const archive_button = document.createElement('button');
  archive_button.classList="btn btn-sm btn-outline-primary"
  archive_button.id = 'archive-button'
  if (!email.archived){
    archive_button.innerHTML = "Archive"
  } else {
    archive_button.innerHTML = "Unarchive"
  }
  archive_button.addEventListener('click', async function() {
      await setArchive(email);
      load_mailbox('inbox')
  });
  document.querySelector('#email-view').appendChild(archive_button)
  }

async function setArchive(email) {
  await fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  })

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      console.log (emails);
      emails.forEach(email => {
      const emailDiv = document.createElement('div');
      let contact = email.sender
      if (mailbox == 'sent'){
        contact = email.recipients
      }
      emailDiv.classList = "list-group-item list-group-item-action"
      emailDiv.innerHTML = `<b>${contact}</b>   ${email.subject}  <span class="float-right">${email.timestamp}</span>`
      if (email.read){
        emailDiv.style.backgroundColor = "Gainsboro";
      }

      emailDiv.addEventListener('click', function() {
        read_email(email);
      })
      document.querySelector("#emails-view").append(emailDiv);
    });

});
}
