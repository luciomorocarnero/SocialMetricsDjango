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

        $('#views-count').textContent = stats.views.toLocaleString('en-US');
        $('#followers-count').textContent = stats.subscribers.toLocaleString('en-US');
        $('#videos-count').textContent = stats.videos.toLocaleString('en-US');
        $('#avgViews-count').textContent = stats.avgViews.toLocaleString('en-US');
        $('#avgLikes-count').textContent = stats.avgLikes.toLocaleString('en-US');
        $('#avgComments-count').textContent = stats.avgComments.toLocaleString('en-US');

        const video_template = $('#video-template');
        const video_container = $('#videos');
        const videos = data.result.videos;
        videos.forEach(e => {
            let clon = document.importNode(video_template.content, true);
            clon.querySelector('.video > span').innerText = e.title;
            clon.querySelector('.video > img').src = e.image;
            clon.querySelector(".video > img").addEventListener('click', () => { window.open(`https://www.youtube.com/watch?v=${e.id}`, '_blank') })
            date = new Date(e.publishedAt);
            clon.querySelector('.video-footer > .video-date').innerText = date.toLocaleString('en-Us', options).replace(',', '');
            clon.querySelector('.video-views').innerText = e.stats.viewCount.toLocaleString('en-US');
            clon.querySelector('.video-comments').innerText = e.stats.commentCount.toLocaleString('en-US');
            clon.querySelector('.video-likes').innerText = e.stats.likeCount.toLocaleString('en-US');
            video_container.appendChild(clon);
        });
    })
    .catch(error => {
        console.error('Hubo un problema con la solicitud fetch:', error);
    })
    .then(
        fetch(url + '&history=3')
            .then(response => {
                if (response.status !== 200) {
                    throw new Error('Error en la red: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                let stats = data.result.profile.stats;
                
                diff(stats.views[0].value,stats.views[1].value,$('#views-count'));
                diff(stats.subscribers[0].value,stats.subscribers[1].value,$('#followers-count'));
                diff(stats.videos[0].value,stats.videos[1].value,$('#videos-count'));
                diff(stats.avgViews[0].value,stats.avgViews[1].value,$('#avgViews-count'));
                diff(stats.avgLikes[0].value,stats.avgLikes[1].value,$('#avgLikes-count'));
                diff(stats.avgComments[0].value,stats.avgComments[1].value,$('#avgComments-count'));

            })
    )

function diff(numeroActual, numeroAnterior, element) {
    const diferencia = numeroActual - numeroAnterior;
    const base = element
    const diferenciaElemento = document.createElement('span');


    if (diferencia > 0) {
        diferenciaElemento.textContent = ` (+${diferencia.toLocaleString('en-US')})`;
        diferenciaElemento.style.color = 'green';
    } else if (diferencia < 0) {
        diferenciaElemento.textContent = ` (${diferencia.toLocaleString('en-US')})`;
        diferenciaElemento.style.color = 'red';
    } else {
        // diferenciaElemento.textContent = ' (+0)';
    }
    base.appendChild(diferenciaElemento);
}
