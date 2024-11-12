const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const url = '/api/instagram?userName=joerogan';

const options = {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
};

Promise.all([
    fetch(url).then(response => {
        if (response.status !== 200) {
            throw new Error('Error en la red: ' + response.status);
        }
        return response.json();
    }),
    fetch(url + '&history=3').then(response => {
        if (response.status !== 200) {
            throw new Error('Error en la red: ' + response.status);
        }
        return response.json();
    })
])
    .then(([data1, data2]) => {
        const profile = data1.result.profile;
        let stats = profile.stats;
        $('#username').textContent = profile.username;
        $('.picture img').src = `data:image/jpeg;base64,${profile.image}`;
        // $(".picture").addEventListener('click', () => {
        //     window.open(`https://x.com/${profile.username}`, '_blank');
        // });

        let statsHistory = data2.result.profile.stats;
        diff(statsHistory.following[0]?.value, statsHistory.following[1]?.value, $('#friends-count'));
        diff(statsHistory.followers[0]?.value, statsHistory.followers[1]?.value, $('#followers-count'));
        diff(statsHistory.media[0]?.value, statsHistory.media[1]?.value, $('#media-count'));
        diff(statsHistory.Avglikes[0]?.value, statsHistory.Avglikes[1]?.value, $('#avgLikes-count'));

        // const tweet_template = $('#tweet-template');
        // const tweet_container = $('#tweets');
        // const tweets = data1.result.posts;
        // tweets.forEach(e => {
        //     let clon = document.importNode(tweet_template.content, true);
        //     clon.querySelector('.video > span').innerText = removeLinks(e.caption);
        //     clon.querySelector('.video > img').src = e.image;
        //     // clon.querySelector('.video').addEventListener('dblclick', () => { window.open(e.url, '_blank') })
        //     date = new Date(e.publishedAt);
        //     clon.querySelector('.video-footer > .video-date').innerText = date.toLocaleString('en-Us', options).replace(',', '');
        //     clon.querySelector('.video-comments').innerText = e.stats.comments.toLocaleString('en-US');
        //     clon.querySelector('.video-likes').innerText = e.stats.likes.toLocaleString('en-US');
        //     tweet_container.appendChild(clon);
        // });

        loadChart('myChart', statsHistory.following, 'Average Following',[153, 55, 200]);
        loadChart('myChart2', statsHistory.followers, 'Average Followers',[54, 162, 235]);
        loadChart('myChart3', statsHistory.media, 'Average Media',[75, 192, 192]);
        loadChart('myChart4', statsHistory.Avglikes, 'Average Likes',[255, 159, 64]);
        loadChart('myChart5', statsHistory.Avgcomments, 'Avgerage Comments',[204, 0, 0]);
    })
    .catch(error => {
        console.error('Hubo un problema con las solicitudes fetch:', error);
    });

function diff(numeroActual, numeroAnterior, element) {
    const diferencia = parseInt(numeroActual, 10) - parseInt(numeroAnterior, 10);
    const base = element
    if (diferencia > 0) {
        base.innerHTML = `${parseInt(numeroActual, 10).toLocaleString('en-US')} <span class="positive">(+${diferencia.toLocaleString('en-US')})</span>`;
    } else if (diferencia < 0) {
        base.innerHTML = `${parseInt(numeroActual, 10).toLocaleString('en-US')} <span class="negative">(${diferencia.toLocaleString('en-US')})</span>`;
    }
    else {
        base.innerHTML = `${parseInt(numeroActual, 10).toLocaleString('en-US')}`;
    }
}

function removeLinks(str) {
    // Expresión regular para buscar URLs
    const regex = /https?:\/\/[^\s]+/g;
    
    // Reemplazar las URLs por una cadena vacía
    return str.replace(regex, '').trim();
  }

function loadChart(selector, data, title, color) {

    const labels = data.map(item => item.date);

    const values = data.map(item => item.value);

    const ctx = document.getElementById(selector).getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    data: values,
                    borderColor: `rgba(${color[0]},${color[1]},${color[2]},1)`,
                    backgroundColor: `rgba(${color[0]},${color[1]},${color[2]},0.3)`,
                    fill: true,
                    yAxisID: 'y'
                },
            ]
        },
        options: {
            manitainAspectRatio: false,
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title,
                    color: getComputedStyle(document.body).getPropertyValue('--color-text'),
                    font: {
                        family: 'Poppins',
                        weight: '600',
                        size: '16px'
                    },
                },
                legend: {
                    display: false,
                }
            },
            scales: {
                x: {
                    type: 'category',
                    title: {
                        display: false
                    },
                    reverse: true,
                    ticks: {
                        color: getComputedStyle(document.body).getPropertyValue('--color-text'),
                    }
                },
                y: {
                    ticks: {
                        color: getComputedStyle(document.body).getPropertyValue('--color-text'),
                    }
                }
            }
        }
    })
}