<script lang="ts">
	import ChatMessage from '$lib/components/ChatMessage.svelte';
	import jarvisDefault from '$lib/images/jarvisDefault.gif';
	import type { ChatCompletionRequestMessage } from 'openai';
	import { SSE } from 'sse.js';
	import { fade } from 'svelte/transition';
	import TimeAndDateDisplay from '$lib/components/TimeAndDateDisplay.svelte';
	import JarvisTriangle from '$lib/components/JarvisTriangle.svelte';
	import Weather from '$lib/components/Weather.svelte';
	import ComlianceLinks from '$lib/components/ComlianceLinks.svelte';

	let query: string = '';
	let answer: string = '';
	let loading: boolean = false;
	let chatMessages: ChatCompletionRequestMessage[] = [];
	let scrollToDiv: HTMLDivElement;

	function scrollToBottom() {
		setTimeout(function () {
			scrollToDiv.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
		}, 100);
	}

	const handleSubmit = async () => {
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

		eventSource.addEventListener('message', (e) => {
			scrollToBottom();
			try {
				loading = false;
				if (e.data === '[DONE]') {
					chatMessages = [...chatMessages, { role: 'assistant', content: answer }];
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
</script>

<svelte:head>
	<title>PLEASE HIRE ME</title>
	<meta name="description" content="Go look at me! my github is /leenpham" />
</svelte:head>

<div class="relative flex flex-col pt-4 w-full px-8 items-center z-0">
	<div class="absolute top-28 bg-cyan-300 rounded-full shadow-cyan-300 shadow-lg -z-10">
		<img
			transition:fade
			class="w-[400px] h-auto rounded-full object-cover aspect-square mix-blend-multiply"
			src={jarvisDefault}
			alt="avatar"
		/>
		<!-- <JarvisTriangle /> -->
		<TimeAndDateDisplay />
		<ComlianceLinks />
		<Weather />
	</div>

	<h1
		class="text-3xl font-bold w-full text-center text-cyan-300 px-2 py-1 border-cyan-200 border rounded-t-3xl shadow-cyan-300 shadow-xl"
	>
		F.L.O.B.O.T.
		<div class="w-full text-cyan-300 tracking-widest text-center text-md font-mono">
			Fortified Log-based Observation and Tracking
		</div>
	</h1>

	<div
		class="h-[650px] w-full bg-gray-900/50 border shadow-lg border-cyan-200 shadow-cyan-300 p-4 overflow-y-auto flex flex-col gap-4"
	>
		<div class="flex flex-col gap-2">
			<ChatMessage type="assistant" message="Hello, how may I assist you today?" />
			{#each chatMessages as message}
				<ChatMessage type={message.role} message={message.content} />
			{/each}
			{#if answer}
				<ChatMessage type="assistant" message={answer} />
			{/if}
			{#if loading}
				<ChatMessage type="assistant" message="Loading.." />
			{/if}
		</div>
		<div class="" bind:this={scrollToDiv} />
	</div>
	<form
		class="flex w-full rounded-b-3xl gap-4 bg-gray-900/50 p-4 shadow-lg shadow-cyan-300 border-cyan-200 border-t-0 border"
		on:submit|preventDefault={() => handleSubmit()}
	>
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
	</form>
</div>
