//================= tag 선언부 =================================
const modal = document.querySelector('#timer-modal');
const floatingTime = document.querySelector('#p-time-text');
const statusBtn = document.querySelector('#status');
const skipBtn = document.querySelector('#btn-skip');
const form = document.recordForm;
const mode = document.querySelector('#interview-mode');
const body = document.querySelector('body');
const inputTexts = document.querySelectorAll('.input-text');

//==============================================================

const timerTime = 1000 * 10;
const end = new Date().getTime() + timerTime;
floatingTime.innerText = Math.floor(timerTime / 1000);

// 시작하자마자 실행될 거
modal.classList.remove('hidden');
skipBtn.classList.add('hidden');

skipBtn.addEventListener('click', function() {
    seconds = 0;
    startInterview();
})

let timerInterval = setInterval(displayTime, 100, end, floatingTime);

function displayTime(endTime, timerTag) {
    let start = new Date().getTime();
    let remain = endTime - start;

    let seconds = Math.floor(remain / 1000.0);
    if(seconds < 0) {
        seconds = 0;
    }

    if(timerTag.getAttribute('id') == 'p-time-text'){
        if(seconds == 0) {
            startInterview();
        }
        timerTag.innerText = seconds;
    }
    else {
        timerTag.innerText = '면접 진행 중... ' + seconds
    }
}

function startInterview() {
    clearInterval(timerInterval);
    modal.classList.add('hidden');
    statusBtn.innerText = '면접 시작';
    statusBtn.click();
    if(mode.innerText == 'True') {
        body.classList.add('background-uncomfortable');
        inputTexts.forEach(function(inputText) {
            inputText.style.color = 'white';
        })
    }
}