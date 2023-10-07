<script lang="ts">
	//@ts-nocheck
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { writable } from 'svelte/store';
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	let isRecording = false;
	let transcript = '';

	let recognition: SpeechRecognition | null = null;
	let wakeWord = 'jarvis'; // Change this to your desired wake word
	let silenceTimeout: NodeJS.Timeout | null = null;

	// Create a writable store for transcript updates
	let transcriptStore = writable('');

	// Function to start recording
	const startRecording = () => {
		if (browser && !isRecording) {
			isRecording = true;
			transcript = '';
			recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
			recognition.lang = 'en-US';
			recognition.continuous = true;
			recognition.interimResults = true;

			recognition.onresult = (event: any) => {
				const result = event.results[event.results.length - 1];
				const spokenText = result[0].transcript.toLowerCase();

				if (spokenText.includes(wakeWord)) {
					clearTimeout(silenceTimeout);
					transcript = spokenText.substring(spokenText.indexOf(wakeWord));
					transcriptStore.set(transcript); // Pass the transcript to the store
				}

				// Reset the silence timeout for each recognized speech
				clearTimeout(silenceTimeout);
				silenceTimeout = setTimeout(() => {
					// If there's silence for 1.5 seconds, stop recognition
					recognition?.stop();
					isRecording = false;
					if (transcript != '') {
						dispatch('transcript', transcript);
					}

					startRecording(); // Restart recognition
				}, 1500); // Adjust the duration for the pause before restarting
			};

			recognition.onend = () => {
				// Restart recognition when it ends
				if (isRecording) {
					startRecording();
				}
			};

			recognition.start();
		}
	};

	onMount(() => {
		// Start recording when the component is mounted
		startRecording();
	});
</script>
