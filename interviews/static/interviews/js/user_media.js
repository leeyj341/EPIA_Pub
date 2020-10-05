//user에게 접근가능한 userMedia가 있는지 검사
//------------------- 선언부 -----------------------

let hdConstraints = {
    video: {
        mandatory: {
            minWidth: 1280,
            minHeight: 720
        }
    },
    audio: true
};

let vgaConstraints = {
    video: {
        mandatory: {
            maxWidth: 640,
            maxHeight: 480
        }
    },
    audio : true
};

//--------------------------------------------------

const time = 1000 * 10;
let interviewEnd
let interviewTimer;

function hasGetUserMedia() {
    return !!(navigator.getUserMedia ||
                navigator.webkitgetUserMedia ||
                navigator.mozGetUserMedia ||
                navigator.msGetUserMedia);
}

let errorCallback = function(err) {
    console.log("다음과 같은 에러가 발생했습니다. : ", err.name);
}

let userMediaStream;
let recordVideo;
let downloadBtn;

if(hasGetUserMedia()) {
    // 있으면 기능 실행
    recordVideo = document.querySelector('#video-record');
    downloadBtn = document.createElement('a');

    userMediaStream = navigator.mediaDevices.getUserMedia(vgaConstraints)
        .then(stream => {
            recordVideo.srcObject = stream;
            downloadBtn.href = stream;
            recordVideo.captureStream = recordVideo.captureStream || recordVideo.mozCaptureStream;
            skipBtn.classList.remove('hidden');

            return new Promise(resolve => recordVideo.onplaying = resolve);
        });
    
    statusBtn.addEventListener('click', interview);
    
} else {
    // 아니면
    alert("현재 브라우저에서 지원하지 않는 기능입니다.")
}

function interview() {
    event.target.innerText = '면접 진행 중';
    event.target.classList.add('animation-btn');
    interviewEnd = new Date().getTime() + time;
    interviewTimer = setInterval(displayTime, 100, interviewEnd, event.target);
    event.target.removeEventListener('click', interview);

    userMediaStream
    .then(() => {
        return startRecording(recordVideo.captureStream(), time)
    })
    .then(recordedChunks => {
        let recordedBlob = new Blob(recordedChunks, {type: "video/webm"});
        // downloadBtn.href = URL.createObjectURL(recordedBlob);
        // downloadBtn.download = "test.wav";
        // downloadBtn.click();
        console.log("Successfully recorded " + recordedBlob.size + " bytes of " +
                    recordedBlob.type + " media.");
        // 타이머 종료
        clearInterval(interviewTimer)
        // 촬영된 결과 서버에 업로드
        upload(recordedBlob);
        // 로딩화면 시작
        loading();
    })
    .catch();
}

function wait(delayInMS) {
    return new Promise(resolve => setTimeout(resolve, delayInMS));
}

function startRecording(stream, lengthInMS) {
    let recorder = new MediaRecorder(stream);
    let data = [];
    
    recorder.ondataavailable = event => data.push(event.data);
    recorder.start();
    console.log(recorder.state + " for " + (lengthInMS/1000) + " seconds...");

    let stopped = new Promise((resolve, reject) => {
        recorder.onstop = resolve;
        recorder.onerror = event => reject(event.name);
    });

    let recorded = wait(lengthInMS).then(
        () => recorder.state == "recording" && recorder.stop()
    );

    return Promise.all([
        stopped,
        recorded
    ]).then(() => data);
}

function getCookie(name) {
    let cookieValue = null;
    if(document.cookie && document.cookie != '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if(cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCurrentTime() {
    let today = new Date();   

    let year = today.getFullYear(); // 년도
    let month = today.getMonth() + 1;  // 월
    let date = today.getDate();  // 날짜
    let day = today.getDay();  // 요일
    let hours = today.getHours(); // 시
    let minutes = today.getMinutes();  // 분
    let seconds = today.getSeconds();  // 초
    let milliseconds = today.getMilliseconds(); // 밀리초

    return month + '-' + date + '_' + hours + minutes + seconds;
}

function upload(blob) {
    let csrftoken = getCookie('csrftoken');
    const questionPk = document.querySelector('#question-pk');
    const answerPk = document.querySelector('#answer-pk');
    const facePk = document.querySelector('#face-pk');
    
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            const json = JSON.parse(xhr.responseText);
            answerPk.value = json.answer_pk;
            facePk.value = json.face_pk;
            sendRequest();
        }
    }

    xhr.open('POST', '/interviews/save_audio/', true);
    xhr.enctype = 'multipart/form-data';
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.setRequestHeader("MyCustomHeader", getCurrentTime() + "_audio");
    
    xhr.upload.onloadend = function() {
        //alert('upload complete');
    }

    let formData = new FormData();
    formData.append('question_pk', questionPk.value);
    formData.append('blob', blob);

    xhr.send(formData);

    
}

function sendRequest() {
    // alert("종료!");
    const form = document.recordForm;
    form.submit();
}