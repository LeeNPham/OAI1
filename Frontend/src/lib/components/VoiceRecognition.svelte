<script lang="ts">
	//@ts-nocheck
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let isRecording = false;
	let transcript = '';
	let transcriptDispatched = false;
	let recognition: SpeechRecognition | null = null;
	let wakeWord = 'jarvis';
	let silenceTimeout: NodeJS.Timeout | null = null;

	// Function to start recording
	const startRecording = () => {
		if (browser && !isRecording) {
			isRecording = true;
			recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
			recognition.lang = 'en-US';
			recognition.continuous = true;
			recognition.interimResults = true;

			recognition.onresult = (event: any) => {
				const result = event.results[event.results.length - 1];
				const spokenText = result[0].transcript.toLowerCase();

				// Reset the flag whenever the wake word is detected again
				if (spokenText.includes(wakeWord)) {
					transcriptDispatched = false;
					clearTimeout(silenceTimeout);
					transcript = spokenText
						.substring(spokenText.indexOf(wakeWord) - 6 + wakeWord.length)
						.trim();
				}

				// Dispatch the transcript if it hasn't been dispatched yet
				if (!transcriptDispatched) {
					if (result.isFinal) {
						console.log('this is the one that has the whole message');
						dispatch('transcript', transcript);
						transcriptDispatched = true;
						transcript = '';
					} else {
						silenceTimeout = setTimeout(() => {
							if (transcript && !transcriptDispatched) {
								console.log('this is the one is thats waiting for the two seconds to happen');
								// dispatch('transcript', transcript);
								transcriptDispatched = true;
								transcript = ''; // Reset the transcript
							}
						}, 2000);
					}
				}
			};

			recognition.onend = () => {
				if (isRecording) {
					recognition?.start();
				}
			};

			recognition.start();
		}
	};

	onMount(() => {
		startRecording();
	});

	onDestroy(() => {
		recognition?.stop();
		isRecording = false;
		clearTimeout(silenceTimeout);
	});
</script>
