import { useState } from "react";
import Stars from "../components/Rating/Stars";
import { canSubmitRating } from "../utils/format";

function localToUtc(value) {
	return new Date(value).toISOString();
}
function defaultDate(hoursAgo) {
	const d = new Date();
	d.setHours(d.getHours() - hoursAgo, 0, 0, 0);
	return d.toISOString().slice(0, 16);
}

export default function RateRoute({ route, onClose, onSubmit }) {
	const [startTime, setStartTime] = useState(defaultDate(2));
	const [endTime, setEndTime] = useState(defaultDate(0));
	const [rating, setRating] = useState(0);
	const [error, setError] = useState("");
	const [submitting, setSubmitting] = useState(false);

	const submit = async (event) => {
		event.preventDefault();

		setError("");

		if (!startTime || !endTime || !rating) {
			setError("Complete all fields to submit a rating.");
			return;
		}

		if (!canSubmitRating(startTime, endTime, rating)) {
			setError("Check the trip dates and times.");
			return;
		}

		setSubmitting(true);
		try {
			await onSubmit({
				route_id: route.id,
				start_time: localToUtc(startTime),
				end_time: localToUtc(endTime),
				rating,
			});
		} catch (err) {
			setError(err.message || "Rating could not be submitted.");
			setSubmitting(false);
		}
	};
	return (
		<div className="modal-backdrop">
			<main className="rating-modal">
				<button className="close-button" onClick={onClose}>
					×
				</button>
				<h1 id="rate-route-title">Rate Route</h1>
				<p className="modal-route-name">{route.name}</p>
				<form onSubmit={submit}>
					<label>
						Start Time
						<input
							type="datetime-local"
							value={startTime}
							max={new Date().toISOString().slice(0, 16)}
							onChange={(event) => setStartTime(event.target.value)}
							required
						/>
					</label>
					<label>
						End Time
						<input
							type="datetime-local"
							value={endTime}
							max={new Date().toISOString().slice(0, 16)}
							onChange={(event) => setEndTime(event.target.value)}
							required
						/>
					</label>
					<fieldset>
						<legend>Rating</legend>
						<Stars value={rating} onChange={setRating} />
					</fieldset>
					{error && <p className="form-error">{error}</p>}
					<button className="primary-button" disabled={submitting}>
						{submitting ? "Submitting…" : "Submit"}
					</button>
				</form>
			</main>
		</div>
	);
}
