<script lang="ts">
	import { PUBLIC_ELEVEN_LABS, PUBLIC_VOICE_ID } from '$env/static/public';
	import jarvisDefault from '$lib/images/Glowing_Orb.gif';
	import axios from 'axios';
	import { onMount } from 'svelte';
	export let message: string;
	export let type: string;

	async function convertTextToSpeech() {
		try {
			if (type === 'user') {
				const response = await axios.post(
					`https://api.elevenlabs.io/v1/text-to-speech/${PUBLIC_VOICE_ID}/stream`,
					{
						text: message,
						model_id: 'eleven_monolingual_v1',
						voice_settings: {
							stability: 0.5,
							similarity_boost: 0.5
						}
					},
					{
						headers: {
							Accept: 'audio/mpeg',
							'Content-Type': 'application/json',
							'xi-api-key': PUBLIC_ELEVEN_LABS
						},
						responseType: 'arraybuffer'
					}
				);
			} else {
				const response = await axios.post(
					`https://api.elevenlabs.io/v1/text-to-speech/${PUBLIC_VOICE_ID}/stream`,
					{
						text: message,
						model_id: 'eleven_monolingual_v1',
						voice_settings: {
							stability: 0.5,
							similarity_boost: 0.5
						}
					},
					{
						headers: {
							Accept: 'audio/mpeg',
							'Content-Type': 'application/json',
							'xi-api-key': PUBLIC_ELEVEN_LABS
						},
						responseType: 'arraybuffer'
					}
				);

				const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
				const audioUrl = URL.createObjectURL(audioBlob);

				const audioElement = new Audio();
				audioElement.src = audioUrl;
				audioElement.controls = true;
				audioElement.play();
			}
		} catch (error) {
			console.error('Error converting text to speech:', error);
		}
	}

	onMount(() => {
		if (message !== 'Loading..') {
			convertTextToSpeech();
		}
	});
</script>

<button
	class="min-w-[60px] {type === 'user' ? 'pointer-events-none' : ''}"
	on:click={convertTextToSpeech}
	><img
		class="h-14 min-w-14 rounded-full object-cover aspect-square {type === 'user'
			? ''
			: 'mix-blend-exclusion'}"
		src={type === 'user' ? 'https://ui-avatars.com/api/?name=Me' : jarvisDefault}
		alt="{type} avatar"
	/></button
>
