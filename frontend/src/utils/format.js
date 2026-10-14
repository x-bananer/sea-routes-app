export function formatNumber(value) {
	return Number.isInteger(value)
		? String(value)
		: Number(value).toFixed(1).replace(/\.0$/, "");
}

export function canSubmitRating(startTime, endTime, rating) {
	return Boolean(
		startTime &&
		endTime &&
		rating &&
		new Date(endTime) > new Date(startTime) &&
		new Date(endTime) <= new Date(),
	);
}
