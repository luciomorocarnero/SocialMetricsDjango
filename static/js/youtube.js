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
        $('#username').textContent = profile.name;
        $('.picture img').src = profile.image;
        $(".picture").addEventListener('click', () => {
            window.open(`https://www.youtube.com/channel/${profile.id}`, '_blank');
        });

        let statsHistory = data2.result.profile.stats;
        diff(statsHistory.views[0].value, statsHistory.views[1].value, $('#views-count'));
        diff(statsHistory.subscribers[0].value, statsHistory.subscribers[1].value, $('#followers-count'));
        diff(statsHistory.videos[0].value, statsHistory.videos[1].value, $('#videos-count'));
        diff(statsHistory.avgViews[0].value, statsHistory.avgViews[1].value, $('#avgViews-count'));
        diff(statsHistory.avgLikes[0].value, statsHistory.avgLikes[1].value, $('#avgLikes-count'));
        diff(statsHistory.avgComments[0].value, statsHistory.avgComments[1].value, $('#avgComments-count'));

        const video_template = $('#video-template');
        const video_container = $('#videos');
        const videos = data1.result.videos;
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

        loadChart('myChart', statsHistory.avgViews, 'Average Views',[153, 55, 200]);
        loadChart('myChart2', statsHistory.avgLikes, 'Average Likes',[54, 162, 235]);
        loadChart('myChart3', statsHistory.avgComments, 'Average Comments',[75, 192, 192]);
        loadChart('myChart4', statsHistory.subscribers, 'Followers',[255, 159, 64]);
        loadChart('myChart5', statsHistory.views, 'Views',[204, 0, 0]);
        loadChart('myChart6', statsHistory.videos, 'Videos',[255, 99, 132]);
    })
    .catch(error => {
        console.error('Hubo un problema con las solicitudes fetch:', error);
    });

function diff(numeroActual, numeroAnterior, element) {
    const diferencia = numeroActual - numeroAnterior;
    const base = element
    if (diferencia > 0) {
        base.innerHTML = `${numeroActual.toLocaleString('en-US')} <span class="positive">(+${diferencia.toLocaleString('en-US')})</span>`;
    } else if (diferencia < 0) {
        base.innerHTML = `${numeroActual.toLocaleString('en-US')} <span class="negative">(${diferencia.toLocaleString('en-US')})</span>`;
    }
    else {
        base.innerHTML = `${numeroActual.toLocaleString('en-US')}`;
    }
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
