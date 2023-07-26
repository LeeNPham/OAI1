<script>
	import { onMount } from 'svelte';
	import { PUBLIC_WEATHER_API } from '$env/static/public';
	let weatherData = null;
	let userLocation = '';
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	onMount(async () => {
		// Retrieve user's location using Geolocation API
		navigator.geolocation.getCurrentPosition(async (position) => {
			const { latitude, longitude } = position.coords;

			// Fetch weather data using latitude and longitude
			const apiKey = PUBLIC_WEATHER_API;
			const apiUrl = `https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${latitude},${longitude}`;

			const response = await fetch(apiUrl);
			const data = await response.json();

			// Set weather data and user location
			weatherData = data.current;
			userLocation = data.location;
			dispatch('weatherData', weatherData);
			dispatch('userLocation', userLocation);
		});
	});
</script>

{#if weatherData && userLocation}
	<div
		class="text-cyan-300 w-[200px] bg-cyan-300/10 shadow-2xl shadow-cyan-300/20 text-center flex flex-col gap-1 p-4 border border-x-4 border-y-2 border-cyan-300 rounded-r-3xl rounded-bl-3xl"
	>
		<div
			class="font-bold border-l-2 border-b-4 border border-cyan-200 px-2 bg-black/90 rounded-tr-2xl"
		>
			<div class="underline">Location:</div>
			<div>{userLocation.name}</div>
		</div>
		<div class="font-bold border-l-2 border-b-4 border border-cyan-200 px-2 bg-black/90">
			<div class="underline">Temperature:</div>
			<div>{weatherData.temp_c}°C</div>
		</div>
		<div class="font-bold border-l-2 border-b-4 border border-cyan-200 px-2 bg-black/90">
			<div class="underline">Condition:</div>
			<div>{weatherData.condition.text}</div>
		</div>
		<div
			class="font-bold border-l-2 border-b-4 border border-cyan-200 px-2 bg-black/90 rounded-br-2xl"
		>
			<div class="underline">Humidity:</div>
			<div>{weatherData.humidity}%</div>
		</div>
	</div>
{:else}
	<div>Loading weather information...</div>
{/if}
