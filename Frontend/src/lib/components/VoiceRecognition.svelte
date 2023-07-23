<script lang="ts">
	import { browser } from '$app/environment';

	let isRecording = false;
	let transcript = '';

	let recognition: SpeechRecognition | null = null;

	const startRecording = () => {
		if (browser && !isRecording) {
			isRecording = true;
			transcript = '';

			recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
			recognition.lang = 'en-US';
			recognition.continuous = true;
			recognition.interimResults = true;

			recognition.onresult = (event) => {
				const result = event.results[event.results.length - 1];
				transcript = result[0].transcript;
			};

			recognition.start();
		}
	};

	const stopRecording = () => {
		if (browser && recognition && isRecording) {
			isRecording = false;
			recognition.stop();
		}
	};
</script>

<div class="flex flex-col items-center justify-center">
	<div class="text-white">Voice Recognition only works with Google Chrome</div>
</div>
<div>
	<button
		class="text-white bg-gray-500 px-2 py-1"
		on:touchstart={startRecording}
		on:touchend={stopRecording}
		on:mousedown={startRecording}
		on:mouseup={stopRecording}
	>
		{isRecording ? 'Recording...' : 'Hold to Record'}
	</button>
	<textarea class="text-black" bind:value={transcript} disabled />
</div>
