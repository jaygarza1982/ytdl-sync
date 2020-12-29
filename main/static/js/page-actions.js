//This file contains actions that take place on the front end side of things

function removePlaylist(playlistId) {
    document.getElementById(playlistId).outerHTML = '';
}

function addPlaylist() {
    let template = document.getElementById('playlist-hidden');
    let templateClone = template.cloneNode(true);

    //The random id is a random number with the dot replaced with nothing
    let randID = (Math.random() + '').replace(/\./g, '');
    templateClone.setAttribute('class', 'row');
    templateClone.setAttribute('id', 'playlist-' + randID);

    let playlists = document.getElementById('playlists');
    playlists.appendChild(templateClone);

    //Set the text input id
    document.querySelector('#playlist-' + randID + ' div input').setAttribute('id', 'playlist-' + randID + '-url');

    //Set the on click event for removing text field
    document.querySelector('#playlist-' + randID + ' div a').setAttribute('onclick', 'removePlaylist("playlist-' + randID + '")');
}