<script lang="ts">
	import { browser } from '$app/environment';

	let isRecording = false;
	export let transcript = '';
	// @ts-ignore
	let recognition: SpeechRecognition | null = null;

	// $: {
	// 	if (transcript) {
	// 		console.log(transcript);
	// 	}
	// }

	const startRecording = () => {
		if (browser && !isRecording) {
			isRecording = true;
			transcript = '';
			// @ts-ignore
			recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
			recognition.lang = 'en-US';
			recognition.continuous = true;
			recognition.interimResults = true;

			recognition.onresult = (event: any) => {
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

	const clearTranscript = () => {
		transcript = '';
	};
</script>

<div class="flex flex-col items-end justify-end w-full">
	<!-- <div class="text-white">Voice Recognition only works with Google Chrome</div> -->
	<!-- Consider giving this value a wake word so that recording is only occuring for transcribed messages when event is created -->
	<div>
		<button
			class="text-cyan-300 border border-cyan-300 px-2 py-1 w-[140px] rounded-md hover:bg-cyan-300/20 font-bold shadow-md shadow-cyan-300"
			on:touchstart={startRecording}
			on:touchend={stopRecording}
			on:mousedown={startRecording}
			on:mouseup={stopRecording}
		>
			{isRecording ? 'Recording...' : 'Hold to Record'}
		</button>
		<button
			class="text-red-300 border border-cyan-300 px-2 py-1 w-[140px] rounded-md hover:bg-cyan-300/20 font-bold shadow-md shadow-cyan-300"
			on:click={clearTranscript}
		>
			Clear Transcript
		</button>
		<!-- This is used to verify the data as being entered <textarea class="text-black" bind:value={transcript} disabled /> -->
	</div>
</div>
