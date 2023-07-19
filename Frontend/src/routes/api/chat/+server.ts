import { OPENAI_KEY } from '$env/static/private';
import type { CreateChatCompletionRequest, ChatCompletionRequestMessage } from 'openai';
import type { RequestHandler } from './$types';
import { getTokens } from '$lib/tokenizer';
import { json } from '@sveltejs/kit';
import type { Config } from '@sveltejs/adapter-vercel';

export const config: Config = {
	runtime: 'edge'
};

export const POST: RequestHandler = async ({ request }) => {
	try {
		if (!OPENAI_KEY) {
			throw new Error('OPENAI_KEY env variable not set');
		}

		const requestData = await request.json();

		if (!requestData) {
			throw new Error('No request data');
		}

		const reqMessages: ChatCompletionRequestMessage[] = requestData.messages;

		if (!reqMessages) {
			throw new Error('no messages provided');
		}

		let tokenCount = 0;

		reqMessages.forEach((msg) => {
			const tokens = getTokens(msg.content);
			tokenCount += tokens;
		});

		const moderationRes = await fetch('https://api.openai.com/v1/moderations', {
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${OPENAI_KEY}`
			},
			method: 'POST',
			body: JSON.stringify({
				input: reqMessages[reqMessages.length - 1].content
			})
		});
		if (!moderationRes.ok) {
			const err = await moderationRes.json();
			throw new Error(err.error.message);
		}

		const moderationData = await moderationRes.json();
		const [results] = moderationData.results;

		if (results.flagged) {
			throw new Error('Query flagged by openai');
		}

		const prompt =
			"You are a virtual assistant for a company called TOZ, we are a cybersecurity and web-innovations company. Your name is FloBot and you will always refer to me as 'sir'. You are also a professional in cybersecurity, its implementation, and compliance with any system and have a background based on data compiled from NIST, HIPAA, SOX, various industry standard cybersecurity protocols, and GLBA datasets. You don't store questions due to security risks and liabilities that might occur during an attack. You are a professional in terms of providing the highest level of customer service and are trained on all things related to TOZ(formerly named Tozny Inc), developer documentation, SDKs, Authorization, Authentication, and hardware tokens that utilize FIDO 2 protocols.";
		tokenCount += getTokens(prompt);

		if (tokenCount >= 4000) {
			throw new Error('Query too large');
		}

		const messages: ChatCompletionRequestMessage[] = [
			{ role: 'system', content: prompt },
			...reqMessages
		];

		const chatRequestOpts: CreateChatCompletionRequest = {
			model: 'gpt-3.5-turbo',
			messages,
			temperature: 0.9,
			stream: true
		};

		const chatResponse = await fetch('https://api.openai.com/v1/chat/completions', {
			headers: {
				Authorization: `Bearer ${OPENAI_KEY}`,
				'Content-Type': 'application/json'
			},
			method: 'POST',
			body: JSON.stringify(chatRequestOpts)
		});

		if (!chatResponse.ok) {
			const err = await chatResponse.json();
			throw new Error(err.error.message);
		}

		return new Response(chatResponse.body, {
			headers: {
				'Content-Type': 'text/event-stream'
			}
		});
	} catch (err) {
		console.error(err);
		return json({ error: 'There was an error processing your request' }, { status: 500 });
	}
};
