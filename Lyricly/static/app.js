const APIController = (function() {
    
    const clientId = '0815ec5573d24c9a9a9daf0fc685ef0a';
    const clientSecret = 'f0a373cb41ad4729b9742b49c2eda8e0';

    // private methods
    const _getToken = async () => {

        const result = await fetch('https://accounts.spotify.com/api/token', {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/x-www-form-urlencoded', 
                'Authorization' : 'Basic ' + btoa(clientId + ':' + clientSecret)
            },
            body: 'grant_type=client_credentials'
        });

        const data = await result.json();
        return data.access_token;
    }

    const _searchTrack = async (token, query) => {

        const result = await fetch(`https://api.spotify.com/v1/search?query=${query}&type=track&offset=0&limit=5`, {
            method: 'GET',
            headers: { 'Authorization' : 'Bearer ' + token}
        });

        const data = await result.json();
        return data.tracks.items;
    }

    

    return {
        getToken() {
            return _getToken();
        },
        searchTrack(token, query) {
            return _searchTrack(token, query);
        }
    }
})();


// UI Module
const UIController = (function() {

    //object to hold references to html selectors
    const DOMElements = {
        hfToken: '#hidden_token',
        searchInput: '#search_input',
        buttonInput: '#btn_search',
        dropdown: '#dropdown',
        buttonAnalyze: '#btn_analyze'
    }

    //public methods
    return {

        //method to get input fields
        inputField() {
            return {
                buttonInput: document.querySelector(DOMElements.buttonInput),
                searchInput: document.querySelector(DOMElements.searchInput),
                dropdown: document.querySelector(DOMElements.dropdown),
                buttonAnalyze: document.querySelector(DOMElements.buttonAnalyze),
            }
        },
        
        createSearchTrack() {
            console.log("tbd")
        },
        
        storeToken(value) {
            document.querySelector(DOMElements.hfToken).value = value;
        },

        getStoredToken() {
            return {
                token: document.querySelector(DOMElements.hfToken).value
            }
        }
    }

})();

const APPController = (function(UICtrl, APICtrl) {

    // get input field object ref
    const DOMInputs = UICtrl.inputField();
    const songsSelected = [];

    // get genres on page load
    const initialize = async () => {
        //get the token
        const token = await APICtrl.getToken();           
        //store the token onto the page
        UICtrl.storeToken(token);
        //get the genres
        // const genres = await APICtrl.getGenres(token);
        //populate our genres select element
        // genres.forEach(element => UICtrl.createGenre(element.name, element.id));
    }
    
    DOMInputs.searchInput.addEventListener('input', async (e) => {
        // prevent page reset
        e.preventDefault();
        // UICtrl.resetTrackDetail();
        // get the token
        const token = UICtrl.getStoredToken().token;
        // get the track endpoint
        console.log(DOMInputs.searchInput.value);
        var query = DOMInputs.searchInput.value;
        console.log(query.replace(/\s/g, '%20'));
        //get the track object
        const track = await APICtrl.searchTrack(token, query);
        // // load the track details
        //  UICtrl.createSearchTrack(track);
        DOMInputs.dropdown.textContent = '';
        track.forEach((track)=> {
            console.log(track.name + " by: " + track.artists[0].name);
            const tr = document.createElement('li');
            tr.innerText = `${track.name}: by ${track.artists[0].name}`;
            tr.onclick = ((e)=> {
                songsSelected.push({title: track.name, artist: track.artists[0].name});
                console.log(songsSelected);
            });
            DOMInputs.dropdown.appendChild(tr);
        });
        // localStorage.setItem('song',`${track[0].name}`);
        // localStorage.setItem('artist',`${track[0].artists[0].name}`);

    });


    DOMInputs.buttonInput.addEventListener('click', async (e) => {

        e.preventDefault();

        // const song = localStorage.getItem('song');
        // const artist = localStorage.getItem('artist');
        const song = songsSelected[0].title;
        console.log(song)
        const artist = songsSelected[0].artist;
        console.log(artist)
        console.log(JSON.stringify({"title": song, "artist": artist}))
    

        fetch('/song', {

            // Specify the method
            method: 'POST',

            // Declare what type of data we're sending
            headers: {"Content-type": "application/json; charset=UTF-8"},
        
            // A JSON payload
            body: JSON.stringify({"title": song, "artist": artist})
            })
            .then(response => response.json())
            .then(json => console.log(json));

    });

    DOMInputs.buttonAnalyze.addEventListener('click', async (e) => {

        e.preventDefault();

        console.log(JSON.stringify(songsSelected));

        fetch('/word_count', {

            // Specify the method
            method: 'POST',

            // Declare what type of data we're sending
            headers: {"Content-type": "application/json; charset=UTF-8"},
        
            // A JSON payload
            body: JSON.stringify(songsSelected)
            })
            .then(response => response.json())
            .then(json => console.log(json));


    });



    return {
        init() {
            console.log('App is starting');
            initialize();
        }
    }

})(UIController, APIController);



// will need to call a method to load token
APPController.init();




