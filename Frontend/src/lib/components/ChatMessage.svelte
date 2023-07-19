<!-- <script lang="ts">
	import type { ChatCompletionRequestMessageRoleEnum } from 'openai';
	export let type: ChatCompletionRequestMessageRoleEnum;
	export let message: any | string;
	import jarvisDefault from '$lib/images/Glowing_Orb.gif';
	import SvelteMarkdown from 'svelte-markdown';
	import { onMount } from 'svelte';
</script>

<div class="flex {type === 'user' ? 'flex-row-reverse' : 'flex-row'} w-full px-10">
	<img
		class="h-14 min-w-14 rounded-full object-cover aspect-square mix-blend-exclusion"
		src={type === 'user' ? 'https://ui-avatars.com/api/?name=Me' : jarvisDefault}
		alt="{type} avatar"
	/>

	<div class="p-2">
		<div class="text-white text-sm {type === 'user' ? 'text-end' : ''}">
			{type === 'user' ? 'Me' : 'Jarvis'}
		</div>
		<div
			class="px-5 py-2 indent-4 {type === 'user'
				? 'rounded-l-2xl rounded-b-2xl bg-gray-800/50 text-pink-400'
				: 'rounded-r-2xl rounded-b-2xl bg-gray-800/50 text-cyan-300'}"
		>
			<SvelteMarkdown source={message} />
		</div>
	</div>
</div> -->

<script lang="ts">
	import type { ChatCompletionRequestMessageRoleEnum } from 'openai';
	export let type: ChatCompletionRequestMessageRoleEnum;
	export let message: any | string;
	import jarvisDefault from '$lib/images/Glowing_Orb.gif';
	import SvelteMarkdown from 'svelte-markdown';
	import { onMount } from 'svelte';

	let isSpeaking = false;

	const synth = window.speechSynthesis;
	const utterance = new SpeechSynthesisUtterance(message);

	utterance.onstart = () => {
		isSpeaking = true;
	};

	utterance.onend = () => {
		isSpeaking = false;
	};

	const speak = () => {
		if (!isSpeaking) {
			synth.speak(utterance);
		} else {
			synth.cancel();
		}
	};
</script>

<!-- svelte-ignore a11y-interactive-supports-focus -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="flex {type === 'user' ? 'flex-row-reverse' : 'flex-row'} w-full px-10">
	<img
		class="h-14 min-w-14 rounded-full object-cover aspect-square mix-blend-exclusion"
		src={type === 'user' ? 'https://ui-avatars.com/api/?name=Me' : jarvisDefault}
		alt="{type} avatar"
	/>

	<div class="p-2">
		<div class="text-white text-sm {type === 'user' ? 'text-end' : ''}">
			{type === 'user' ? 'Me' : 'Jarvis'}
		</div>
		<div
			role="button"
			aria-label="Toggle speech"
			on:click={() => speak()}
			class="px-5 py-2 indent-4 {type === 'user'
				? 'rounded-l-2xl rounded-b-2xl bg-gray-800/50 text-pink-400'
				: 'rounded-r-2xl rounded-b-2xl bg-gray-800/50 text-cyan-300'}"
		>
			<SvelteMarkdown source={message} />
		</div>
	</div>
</div>
