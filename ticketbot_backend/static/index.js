const recordBtn = document.getElementById('recordBtn');
const statusEl = document.getElementById('status');
const transcriptEl = document.getElementById('transcript');
const formEl = document.querySelector('form[action="/ask"][method="post"]');
const inputEl = document.querySelector('input[name="user_input"]');

let mediaRecorder;
let chunks = [];

recordBtn.addEventListener('click', async () => {
  try {
    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      chunks = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) chunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('file', blob, 'speech.webm');

        statusEl.textContent = 'Transcribing your speech...';
        transcriptEl.textContent = '';

        try {
          const res = await fetch('/api/transcribe', { method: 'POST', body: formData });
          const data = await res.json();

          if (!res.ok) {
            statusEl.textContent = `Error: ${data.error || 'Unknown error'}`;
            return;
          }

          const transcript = data.transcript || '';
          transcriptEl.textContent = transcript ? `Transcript: ${transcript}` : 'No speech detected. Try again.';
          if (transcript && inputEl && formEl) {
            inputEl.value = transcript;
            formEl.submit();
          }
        } catch (err) {
          console.error('Upload/transcription failed:', err);
          statusEl.textContent = 'Upload/transcription failed. Check console.';
        }
      };

      mediaRecorder.start();
      recordBtn.textContent = 'Stop Recording';
      statusEl.textContent = 'Recording... Click again to stop.';
    } else {
      mediaRecorder.stop();
      recordBtn.textContent = 'Start Recording';
    }
  } catch (err) {
    console.error('Microphone error:', err);
    statusEl.textContent = 'Microphone permission denied or not available.';
  }
});
