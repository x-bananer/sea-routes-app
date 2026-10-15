const API_BASE_URL = "https://74cmv85mek.execute-api.us-east-1.amazonaws.com/production";

async function request(path, options) {
	const response = await fetch(`${API_BASE_URL}${path}`, options);

	if (!response.ok) {
		let message = "Request could not be completed.";
		try {
			const data = await response.json();
			message = data.error || message;
		} catch {
			// Keep the default message when the response has no JSON body.
		}
		throw new Error(message);
	}

	return response.status === 204 ? null : response.json();
}

export async function getRoutes() {
	return request("/routes");
}

export async function getRouteDetails(routeId) {
	return request(`/routes/${routeId}`);
}

export async function saveRating(routeId, rating) {
	return request(`/routes/${routeId}/ratings`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(rating),
	});
}
