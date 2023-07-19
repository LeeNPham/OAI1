<script>
	import { onMount } from 'svelte';

	let weatherData = null;
	let userLocation = '';

	onMount(async () => {
		// Retrieve user's location using Geolocation API
		navigator.geolocation.getCurrentPosition(async (position) => {
			const { latitude, longitude } = position.coords;

			// Fetch weather data using latitude and longitude
			const apiKey = '61883d2adbd44cf48f872347231907';
			const apiUrl = `https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${latitude},${longitude}`;

			const response = await fetch(apiUrl);
			const data = await response.json();

			// Set weather data and user location
			weatherData = data.current;
			userLocation = data.location.name;
		});
	});
</script>

{#if weatherData && userLocation}
	<div
		class="text-cyan-300 w-[200px] bg-cyan-300/10 shadow-2xl shadow-cyan-300/20 text-center flex flex-col gap-1 absolute -bottom-20 -left-56 p-4 border border-x-4 border-y-2 border-cyan-300 rounded-r-3xl rounded-bl-3xl"
	>
		<div class="underline">Location:</div>
		<div>{userLocation}</div>
		<div class="underline">Temperature:</div>
		<div>{weatherData.temp_c}°C</div>
		<div class="underline">Condition:</div>
		<div>{weatherData.condition.text}</div>
		<div class="underline">Humidity:</div>
		<div>{weatherData.humidity}%</div>
	</div>
{:else}
	<div>Loading weather information...</div>
{/if}
