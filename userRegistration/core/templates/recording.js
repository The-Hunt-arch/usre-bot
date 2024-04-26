var recordedAudioDict = {};
// Function to start recording
function startRecording(button, audioElement, questionIndex) {
    console.log("Starting recording for question index:", questionIndex);
    console.log("audioelement", audioElement);

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            recorder = new MediaRecorder(stream);
            var chunks = []; // Array to store audio chunks

            recorder.ondataavailable = e => {
                chunks.push(e.data); // Store each chunk of audio data
            };

            recorder.onstop = () => {
                // Combine all audio chunks into a single Blob
                var audioBlob = new Blob(chunks, { type: 'audio/wav' });

                
                // Save the audio Blob to local storage
                var audioKey = 'question_' + questionIndex;
                localStorage.setItem(audioKey, audioBlob);

                // Create a URL for the audio Blob
                var audioUrl = URL.createObjectURL(audioBlob);

                // Set the audio element source and display it
                audioElement.src = audioUrl;
                audioElement.style.display = 'block';
                console.log(audioElement)
                console.log("audio")

                // Update button text and style
                // Toggle the data-state attribute value
                button.setAttribute('data-state', button.getAttribute('data-state') === 'start' ? 'stopped' : 'start');
                button.classList.remove('btn-danger');
                button.classList.add('btn-primary');

                // Store the audio URL in a hidden input field for form submission
                button.closest('.container').querySelector('input[type="hidden"]').value = audioUrl;

                
            };

            button.setAttribute('data-state','stopped') // Update button text content here
            button.classList.remove('btn-primary');
            button.classList.add('btn-danger');
            recorder.start();

            // Start recording when the button is clicked
            button.onclick = function() {
                if (recorder.state === 'inactive') {
                    chunks = []; // Reset chunks array for each recording session
                    recorder.start();
                    button.setAttribute('data-state','stopped') // Update button text content
                    button.classList.remove('btn-primary');
                    button.classList.add('btn-danger');
                } else {
                    recorder.stop(); // Stop recording
                }
            };
        })
        .catch(console.error);
}

// Function to stop recording
function stopRecording(button) {
    console.log("yes")
    if (recorder.state === 'recording') {
        recorder.stop();
        button.setAttribute('data-state','start')
        button.classList.remove('btn-danger');
        button.classList.add('btn-primary');
    }
}
