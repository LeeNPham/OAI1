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
			transcriptDispatched = false;
			recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
			recognition.lang = 'en-US';
			recognition.continuous = true;
			recognition.interimResults = true;

			recognition.onresult = (event: any) => {
				const result = event.results[event.results.length - 1];
				const spokenText = result[0].transcript.toLowerCase();

				// When the wake word is detected, start capturing the transcript
				if (spokenText.includes(wakeWord) && !transcriptDispatched) {
					clearTimeout(silenceTimeout);
					transcript = spokenText.substring(spokenText.indexOf(wakeWord) + wakeWord.length).trim();

					// If the result is finalized by the speech recognition, dispatch it
					if (result.isFinal) {
						dispatch('transcript', transcript);
						transcriptDispatched = true;
						transcript = '';
					} else {
						// If not, wait for silence and then dispatch
						silenceTimeout = setTimeout(() => {
							if (transcript && !transcriptDispatched) {
								dispatch('transcript', transcript);
								transcriptDispatched = true;
							}
							transcript = ''; // Reset the transcript
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
