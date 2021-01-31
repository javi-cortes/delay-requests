<script>
import dayjs from "dayjs"
import { onMount } from "svelte"
import { sleep } from "./utils"
	let request_url
	let date
	let http_verb
	let requests = getRequests()
	let minDate = calculateMinDate()

	async function storeRequest() {
		await fetch("http://localhost:8000/api/requests/", {
			method: "post",
			body: JSON.stringify({
				url: request_url,
				datetime: new Date(date).toISOString(),
				http_verb: http_verb,
			}),
			headers: {
				"content-type": "application/json",
			},
		})
		requests = getRequests()
		// date = request_url = ""
	}
		
	async function getRequests() {
		const res = await fetch("http://localhost:8000/api/requests/")
		return await res.json()
	}

	function calculateMinDate(){
		return dayjs().add(1, "minute").format("YYYY-MM-DDTHH:mm")
	}

	onMount(async () => {		
		/**
		 * Keep updating the minimum time
		 */
		const secondsLeftToNextMinute = 60 - new Date().getSeconds()
		await sleep(secondsLeftToNextMinute * 1000)
		minDate = calculateMinDate()		
		const interval = setInterval(() => {
			minDate = calculateMinDate()	
		}, 60000)						
		
		return () => clearInterval(interval)
	})

</script>

<main>
	<h1>Request delayer</h1>
	<p>Type the request to be delayed</p>
	<form on:submit|preventDefault={storeRequest}>
		<input type="text" bind:value={request_url} required />
		<input type="datetime-local"  min={minDate} max="3000-01-03T09:00" bind:value={date} required />
		<select name="http-verbs" id="http-verbs" bind:value={http_verb}>
			<option value="POST">POST</option>
			<option value="GET">GET</option>
			<option value="HEAD">HEAD</option>
			<option value="PUT">PUT</option>
			<option value="DELETE">DELETE</option>
			<option value="CONNECT">CONNECT</option>
			<option value="OPTIONS">OPTIONS</option>
			<option value="TRACE">TRACE</option>
			<option value="PATCH">PATCH</option>
		</select>
		<input type="submit" />
	</form>

	<h1>Request Log</h1>
	{#await requests}
		Loading
	{:then requestsLoaded}
		<table>
			<tr>
				<th>Request</th>
				<th>Status</th>
				<th>Time</th>
			</tr>
			{#each requestsLoaded as rq}
				<tr>
					<td>
						<pre>{rq.url}</pre>
					</td>
					<td>
						<pre>{rq.state}</pre>
					</td>
					<td>
						<pre>{rq.datetime}</pre>
					</td>
				</tr>
			{/each}
		</table>
	{/await}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
	table {
		margin:auto;
	}
</style>
