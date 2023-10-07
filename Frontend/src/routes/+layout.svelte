<script>
	import { fly, fade } from 'svelte/transition';
	import JarvisTriangle from '$lib/components/JarvisTriangle.svelte';
	import '../app.postcss';
	import './styles.css';
	let showJarvis = false;
	let showOpenButton = false;
</script>

<div class="app bg-black">
	<main>
		{#if showJarvis == true}
			<slot />
		{:else}
			<div class="relative flex items-center justify-center flex-1">
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<!-- svelte-ignore a11y-mouse-events-have-key-events -->
				<div
					transition:fade
					on:mouseover={() => {
						showOpenButton = true;
					}}
					class="border-2 border-red-700 rounded-full hover:shadow-2xl hover:shadow-red-700 relative"
				>
					<JarvisTriangle />
					{#if showOpenButton}
						<button
							transition:fly={{ x: 200, duration: 1000 }}
							class="absolute top-0 right-0 mt-16 -mr-40 text-cyan-300 hover:text-white/90 font-bold shadow-md border border-cyan-300/50 hover:bg-cyan-300 shadow-cyan-300 px-4 py-1 rounded-xl"
							type="button"
							on:click={() => {
								showJarvis = true;
							}}>Open Jarvis</button
						>
					{/if}
				</div>
			</div>
		{/if}
	</main>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		overflow-x: hidden; /* Prevent horizontal overflow */
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 1275px;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>
