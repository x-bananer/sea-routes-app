const API_BASE_URL = "https://74cmv85mek.execute-api.us-east-1.amazonaws.com/production";

export async function getRoutes() {
	const response = await fetch(`${API_BASE_URL}/routes`);

	if (!response.ok) {
		throw new Error("Routes could not be loaded.");
	}

	return response.json();
}
