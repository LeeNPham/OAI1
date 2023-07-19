<script lang="ts">
	import type { ChatCompletionRequestMessageRoleEnum } from 'openai';
	import SvelteMarkdown from 'svelte-markdown';
	import AudioPlayer from './AudioPlayer.svelte';
	export let type: ChatCompletionRequestMessageRoleEnum;
	export let message: any | string;
</script>

<div class="flex items-start {type === 'user' ? 'flex-row-reverse' : 'flex-row'} w-full px-10">
	<AudioPlayer {type} {message} />

	<div class="p-2">
		<div class="text-white text-sm {type === 'user' ? 'text-end' : ''}">
			{type === 'user' ? 'Me' : 'Jarvis'}
		</div>
		<div
			class="px-5 py-2 indent-4 {type === 'user'
				? 'rounded-l-2xl rounded-b-2xl bg-gray-800/70 text-pink-400'
				: 'rounded-r-2xl rounded-b-2xl bg-gray-800/70 text-cyan-300'}"
		>
			<SvelteMarkdown source={message} />
		</div>
	</div>
</div>
