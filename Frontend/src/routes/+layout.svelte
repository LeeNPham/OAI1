<script>
	import '../app.postcss';
	import './styles.css';
</script>

<div class="app bg-black">
	<main>
		<slot />
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
