document.addEventListener('DOMContentLoaded', function() {
    let form = document.querySelector('#chatForm');
    let field = document.querySelector('#messenger');
    let room = document.querySelector('#chatroom');
    let failed = document.querySelector('#errorx');

    if (room) {

        // scroll to the bottom
        let xH = room.scrollHeight;
        room.scrollTo(0, xH);

        // https://stackoverflow.com/a/33641432
        // var log = $('#chatroom'); * taken from stackoverflow
        // log.animate({ scrollTop: log.prop('scrollHeight')}, 0); * taken from stackoverflow

        // get latest messages at each interval
        let interval = setInterval(() => {
            getLatest(room, interval, failed)
        }, 1000)

    }

    if (form) {
        // on form submit send the message to the server
        form.addEventListener('submit', (e) => {
            e.preventDefault()

            fetch('/send', {
                credentials: "same-origin",
                method: "POST",
                headers: {
                    'X-CSRFToken' : getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    message: field.value
                })
            })
            .then(response => response.json())
            .then(response => {
                if (response.message == 'LoginError') {
                    alert('You Need To Login To Perform This Action!')
                }
                
                console.log(response)

                // empty the field value;
                field.value = '';
            })
            .catch(err => {
                console.log(err);
                alert('Something Went Wrong... Please Refresh The Page!')
            })
        })
    }
})

// getting the latest messages from the server
function getLatest(room, interval, failed) {

    // getting the id of the last message in the channel
    lastId = room.lastElementChild.id;
    if (!!lastId == false) {
        lastId = 0;
    }

    // fetching the messages if they exist
    fetch(`/messages/${lastId}`, {
        credentials: 'same-origin',
        method: "GET"
    })
    .then(response => response.json())
    .then(response => {

        // iterating over the obtained data
        response.data.forEach(message => {

            // creating new message divs in the room
            let container = document.createElement('div');
            container.id = message.id;
            container.innerHTML = `
                <div class="message" id="${message.id}">
                    <div class="sender">${message.user.username} :: </div>
                    <div class="sentMessage">${message.message}</div>
                </div>
            `
            // appending to the room
            room.appendChild(container);
            lastId = message.id;

            // scrolling to the bottom of the chat room
            let xH = room.scrollHeight; 
            room.scrollTo(0, xH);
        })
    })
    .catch(err => {
        // error handling
        console.log(err)
        failed.style.display = 'block'
        failed.innerHTML = 'Something Went Wrong... Please Refresh The Page!.'
        clearInterval(interval)
    })

}

// Taken from django docs
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}