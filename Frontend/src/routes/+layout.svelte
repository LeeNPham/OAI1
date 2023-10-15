<script>
	import { fly, fade } from 'svelte/transition';
	import '../app.postcss';
	import './styles.css';
	let showJarvis = false;
	let showOpenButton = false;
</script>

<div class="app bg-gray-100">
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
					<img
						src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/770px-Pok%C3%A9_Ball_icon.svg.png"
						class="rounded-full"
						style="max-width: 770px; height: 431px; margin: 0px; width: 432px;"
						alt="File:Poké Ball icon.svg - Wikipedia"
						aria-hidden="false"
					/>
				</div>
				{#if showOpenButton}
					<button
						transition:fly={{ x: 200, duration: 1000 }}
						class="absolute top-50 right-40 text-red-500 hover:text-white/90 font-bold shadow-md border border-red-500/50 hover:bg-red-500 shadow-red-700 px-4 py-1 rounded-xl"
						type="button"
						on:click={() => {
							showJarvis = true;
						}}>Open PokePal!</button
					>
				{/if}
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
