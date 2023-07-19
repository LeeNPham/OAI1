<script lang='ts'>
	import { PUBLIC_ELEVEN_LABS } from '$env/static/public';
	import axios from 'axios';
	export let message: String

	async function convertTextToSpeech() {
		try {
			const response = await axios.post(
				'https://api.elevenlabs.io/v1/text-to-speech/HqOrzJvDf9jFg9WwqYxG/stream',
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
		} catch (error) {
			console.error('Error converting text to speech:', error);
		}
	}
</script>

<button class="text-white" on:click={convertTextToSpeech}>Convert Text to Speech</button>
