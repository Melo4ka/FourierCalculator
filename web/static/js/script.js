function submit() {
    const data = {}
    const inputs = document.querySelectorAll('input[type=text]')
    Array.from(inputs).forEach(input => data[input.id] = input.value)

    if (isNaN(data.order) || data.order < 1 || data.order > 30) {
        notifyError('Порядок разложения должен быть числом от 1 до 30')
        return
    }

    calculateFourierSeries(data)
}

function calculateFourierSeries(data) {
    fetch('/fourier_series', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw Error()
            }
            return response.text()
        })
        .then(text => {
            const series = document.getElementById('fourier-series')
            series.innerText = '$$' + text + '$$'
            MathJax.typeset()
            drawPlot(data)
        })
        .catch(() => notifyError('Ошибка при вычислении ряда'))
}

function drawPlot(data) {
    const container = document.querySelector('.result')
    fetch('/plot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw Error()
            }
            return response.blob()
        })
        .then(imageBlob => {
            const imageURL = URL.createObjectURL(imageBlob);
            const plot = document.getElementById('plot')
            const img = document.createElement('img')
            img.src = imageURL
            plot.innerHTML = ''
            plot.appendChild(img)

            container.hidden = false
        })
        .catch(() => {
            container.hidden = true
            notifyError('Ошибка при построении графика')
        })
}

function notifyError(message) {
    Swal.fire({
        icon: 'error',
        title: 'Ошибка',
        text: message
    })
}
