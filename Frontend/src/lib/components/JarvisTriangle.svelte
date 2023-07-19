<svg class="absolute top-0 -right-[500px]" width="210" height="210" id="jarvis-like">
	<defs>
		<filter id="light-circle">
			<feGaussianBlur result="blurred" in="SourceGraphic" stdDeviation="1" />
		</filter>
		<!-- <filter id="light-triangle">
        <feGaussianBlur stdDeviation="2" in="SourceGraphic" result="blur2" />
        <feComposite in="SourceAlpha" in2="offOut" operator="arithmetic" k1="1" k2="1" k3="1" k4="0" />
    </filter> -->
	</defs>
	<!-- circle outer -->
	<circle
		cx="105"
		cy="105"
		r="100"
		style="fill: transparent;stroke: #B4F6FB;stroke-width: 2; stroke-dasharray: 50, 5"
	/>
	<circle cx="105" cy="105" r="95" style="fill: transparent;stroke: #64E6EF;stroke-width: 1.5;" />
	<!-- circle dash cool :D -->
	<circle
		cx="105"
		cy="105"
		r="80"
		style="fill: transparent; stroke: #B4F6FB; stroke-width: 10; stroke-dasharray: 2,2.29"
	>
		<animateTransform
			attributeName="transform"
			attributtype="XML"
			type="rotate"
			from="0 105 105"
			to="360 105 105"
			dur="10s"
			repeatCount="indefinite"
		/>
	</circle>
	<circle
		cx="105"
		cy="105"
		r="61"
		transform="rotate(0 105 105)"
		style="fill: transparent; stroke: #B4F6FB; stroke-width: 2; stroke-dasharray: 50, 25"
	>
		<animateTransform
			attributeName="transform"
			attributtype="XML"
			type="rotate"
			from="0 105 105"
			to="-360 105 105"
			dur="10s"
			repeatCount="indefinite"
		/>
	</circle>
	<!-- circle inner -->
	<circle
		cx="105"
		cy="105"
		r="50"
		style="fill: transparent; stroke: #64E6EF; stroke-width: 15;filter: url(#light-circle);"
	/>
	<circle cx="105" cy="105" r="40" style="fill: transparent; stroke: #64E6EF; stroke-width: 2" />
	<!-- triangle primary -->
	<path d="M 105 120 L 130 95 L 80 95 z" style="fill: #D1FBFC; stroke: #B4F6FB; stroke-width:5" />
</svg>
