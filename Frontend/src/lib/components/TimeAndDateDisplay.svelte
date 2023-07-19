<script>
	import { onMount } from 'svelte';

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

<div class="text-cyan-300 text-center absolute top-0 -left-56">
	<div>Current date:</div>
	<div>{currentDate}</div>

	<div>Current time:</div>
	<div>{currentTime}</div>
</div>
