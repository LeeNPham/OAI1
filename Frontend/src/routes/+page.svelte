<script lang="ts">
	import ChatMessage from '$lib/components/ChatMessage.svelte';
	import jarvisDefault from '$lib/images/jarvisDefault.gif';
	import type { ChatCompletionRequestMessage } from 'openai';
	import { SSE } from 'sse.js';
	import { fade } from 'svelte/transition';
	import TimeAndDateDisplay from '$lib/components/TimeAndDateDisplay.svelte';
	import JarvisTriangle from '$lib/components/JarvisTriangle.svelte';
	import Weather from '$lib/components/Weather.svelte';
	import VoiceRecognition from '$lib/components/VoiceRecognition.svelte';

	let query: string = '';
	let answer: string = '';
	let loading: boolean = false;
	let chatMessages: ChatCompletionRequestMessage[] = [];
	let scrollToDiv: HTMLDivElement;
	let weatherData: any = null; // Modify the type accordingly
	let userLocation: any = null; // Modify the type accordingly

	function scrollToBottom() {
		setTimeout(function () {
			scrollToDiv.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
		}, 100);
	}

	const handleSubmit = async (e?: { detail: any }) => {
		console.log(e?.detail);

		let transcript;

		if (e) {
			transcript = e.detail;
			query = transcript;
		}

		loading = true;
		chatMessages = [...chatMessages, { role: 'user', content: query }];

		const eventSource = new SSE('/api/chat', {
			headers: {
				'Content-Type': 'application/json'
			},
			payload: JSON.stringify({ messages: chatMessages })
		});

		query = '';
		eventSource.addEventListener('error', handleError);
		eventSource.addEventListener('message', async (e) => {
			scrollToBottom();
			try {
				loading = false;
				if (e.data === '[DONE]') {
					chatMessages = [...chatMessages, { role: 'assistant', content: answer }];

					if (weatherData && userLocation) {
						const weatherMessage = `These are all user details, please don't say anything like Based on the information you provided, I want you to just provide the answer without saying I provided you any data concerning the weather and my location. I want it to be a mystery as to how you know this information. Location: ${JSON.stringify(
							userLocation
						)}, Weather: ${JSON.stringify(weatherData)}`;
						chatMessages = [...chatMessages, { role: 'system', content: weatherMessage }];
					}
					answer = '';
					return;
				}

				const completionResponse = JSON.parse(e.data);
				const [{ delta }] = completionResponse.choices;
				if (delta.content) {
					answer = (answer ?? '') + delta.content;
				}
			} catch (err) {
				handleError(err);
			}
		});

		eventSource.stream();
		scrollToBottom();
	};

	function handleError<T>(err: T) {
		loading = false;
		query = '';
		answer = '';
		console.error(err);
	}

	// Listen for emitted events from Weather component
	const handleWeatherData = (event: { detail: any }) => {
		weatherData = event.detail;
	};

	const handleUserLocation = (event: { detail: any }) => {
		userLocation = event.detail;
	};
</script>

<svelte:head>
	<title>J.A.R.V.I.S</title>
	<meta name="description" content="Go look at me! my github is /leenpham" />
</svelte:head>

<div class="relative flex flex-col w-full px-8 items-center z-0">
	<div class="relative flex flex-row w-full justify-between items-center py-32">
		<div class="flex flex-col gap-2">
			<TimeAndDateDisplay />
			<Weather on:weatherData={handleWeatherData} on:userLocation={handleUserLocation} />
		</div>
		<div class="flex flex-row top-28 bg-cyan-300 rounded-full shadow-cyan-300 shadow-lg -z-10">
			<img
				transition:fade
				class="w-[400px] h-auto rounded-full object-cover aspect-square mix-blend-multiply"
				src={jarvisDefault}
				alt="avatar"
			/>
		</div>
		<JarvisTriangle />
	</div>
	<div
		class="absolute bg-black sm:bg-black/80 lg:bg-transparent h-full flex flex-col max-w-[739px]"
	>
		<h1
			class="text-3xl font-bold w-full text-center text-cyan-300 px-2 py-1 border-cyan-200 border rounded-t-3xl shadow-cyan-300 shadow-xl"
		>
			J.A.R.V.I.S
			<div class="w-full text-cyan-300 tracking-widest text-center text-md font-mono">
				Just A Rather Very Intelligent System
			</div>
		</h1>
		<div
			class="flex-auto w-full bg-gray-900/50 border shadow-lg border-cyan-200 shadow-cyan-300 p-4 overflow-y-auto flex flex-col gap-4"
		>
			<div class="flex flex-col gap-2">
				<ChatMessage type="assistant" message="Hello, how may I assist you today?" />
				{#each chatMessages as message}
					{#if !message.content?.startsWith('These are all user details,')}
						<ChatMessage type={message.role} message={message.content} />
					{/if}
				{/each}
				{#if loading}
					<ChatMessage type="assistant" message="Loading.." />
				{/if}
			</div>
			<div class="" bind:this={scrollToDiv} />
		</div>
		<form
			class="flex flex-col w-full rounded-b-3xl gap-4 bg-gray-900/50 p-4 shadow-lg shadow-cyan-300 border-cyan-200 border-t-0 border"
			on:submit|preventDefault={() => handleSubmit()}
		>
			<div class="flex flex-row gap-5 w-full">
				<input
					type="text"
					class="w-full rounded-full bg-gray-600 text-cyan-300 focus:ring-0 focus:border-0 border-0"
					bind:value={query}
				/>
				<button
					type="submit"
					class="text-cyan-300 shadow-md border border-cyan-300/50 hover:bg-gray-600/10 shadow-cyan-300 px-4 py-1 rounded-xl"
				>
					Send
				</button>
			</div>
		</form>

		<VoiceRecognition on:transcript={handleSubmit} />
	</div>
</div>
