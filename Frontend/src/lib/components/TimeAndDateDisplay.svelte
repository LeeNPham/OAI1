<script>
	import { onMount } from 'svelte';
	import { slide } from 'svelte/transition';

	let currentDate = '';
	let currentTime = '';

	onMount(() => {
		const updateTime = () => {
			const now = new Date();
			currentDate = now.toLocaleDateString();
			currentTime = now.toLocaleTimeString();
		};

		// Update the time every second
		const interval = setInterval(updateTime, 1000);

		// Cleanup the interval on component unmount
		return () => clearInterval(interval);
	});
</script>

<div
	transition:slide
	class="text-cyan-300 w-[200px] bg-cyan-300/10 shadow-2xl shadow-cyan-300/20 text-center flex flex-col gap-1 p-4 pr-2 border border-x-4 border-y-2 border-cyan-300 rounded-r-3xl rounded-bl-3xl"
>
	<div
		class="font-bold border-l-2 border-b-4 border border-cyan-200 px-2 bg-black/90 rounded-tr-2xl"
	>
		<div class="underline">Current date:</div>
		<div>{currentDate}</div>
	</div>
	<div
		class="font-bold border-l-2 border-b-4 border border-cyan-200 px-2 bg-black/90 rounded-br-2xl"
	>
		<div class="underline">Current time:</div>
		<div>{currentTime}</div>
	</div>
</div>
