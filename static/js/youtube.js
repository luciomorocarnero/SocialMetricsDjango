const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const url = '/api/youtube?userName=@joerogan';

const options = {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
};

fetch(url)
    .then(response => {
        if (response.status !== 200) {
            throw new Error('Error en la red: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        const profile = data.result.profile;
        const stats = profile.stats
        $('#username').textContent = profile.name;
        $('.picture img').src = profile.image;
        $(".picture").addEventListener('click', () => {
            window.open(`https://www.youtube.com/channel/${profile.id}`, '_blank');
        })

        $('#views-count').textContent = stats.views.toLocaleString('es-ES');
        $('#followers-count').textContent = stats.subscribers.toLocaleString('es-ES');
        $('#videos-count').textContent = stats.videos.toLocaleString('es-ES');
        $('#avgViews-count').textContent = stats.avgViews.toLocaleString('es-ES');
        $('#avgLikes-count').textContent = stats.avgLikes.toLocaleString('es-ES');
        $('#avgComments-count').textContent = stats.avgComments.toLocaleString('es-ES');
        
        const video_template = $('#video-template');
        const video_container = $('#videos');
        const videos = data.result.videos
        videos.forEach(e => {
            let clon = document.importNode(video_template.content, true);
            clon.querySelector('.video > span').innerText = e.title;
            clon.querySelector('.video > img').src = e.image;
            clon.querySelector(".video > img").addEventListener('click', () => {window.open(`https://www.youtube.com/watch?v=${e.id}`, '_blank')})
            date = new Date(e.publishedAt);
            clon.querySelector('.video-footer > .video-date').innerText = date.toLocaleString('en-Us', options).replace(',','');
            clon.querySelector('.video-views').innerText = e.stats.viewCount.toLocaleString('es-ES');
            clon.querySelector('.video-comments').innerText = e.stats.commentCount.toLocaleString('es-ES');
            clon.querySelector('.video-likes').innerText = e.stats.likeCount.toLocaleString('es-ES');
            video_container.appendChild(clon);
        });

    })
    .catch(error => {
        console.error('Hubo un problema con la solicitud fetch:', error);
    });

