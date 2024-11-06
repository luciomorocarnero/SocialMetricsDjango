const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const url = '/api/youtube?userName=@joerogan';

fetch(url)
    .then(response => {
        if (response.status !== 200) {
            throw new Error('Error en la red: ' + response.status);
        }
        return response.json(); // Parseamos la respuesta JSON
    })
    .then(data => {
        const profile = data.result.profile;
        const stats = profile.stats
        console.log(document.querySelector('#username'))
        $('#username').textContent = profile.name;
        $('.picture img').src = profile.image;

        $('#views').textContent = stats.views
        $('#followers').textContent = stats.subscribers
        $('#videos').textContent = stats.videos
        $('#avgViews').textContent = stats.avgViews
        $('#avgLikes').textContent = stats.avgLikes
        $('#avgComments').textContent = stats.avgComments
    })
    .catch(error => {
        console.error('Hubo un problema con la solicitud fetch:', error);
    });

