//File contains code to interact with server

function updatePlaylists() {
    let playlistURLs = '';

    let inputs = document.getElementsByTagName('input')

    for (let i = 0; i < inputs.length; i++) {
        let currentInput = inputs[i];

        if (currentInput.getAttribute('id').startsWith('playlist') && currentInput.getAttribute('id').endsWith('url')) {
            if (currentInput.value != '')
                playlistURLs += currentInput.value + ',';
        }
    }

    $.post(
        '/update-playlists',
        {
            playlists: playlistURLs,
        },
        function (data, status) {
            if (status == 'success') {
                $('#saved-message').fadeIn();
                $('#saved-message').fadeOut();
            }
        }
    );
}