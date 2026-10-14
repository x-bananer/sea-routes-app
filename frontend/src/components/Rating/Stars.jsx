import starIcon from "../../assets/icons/star.svg";

export default function Stars({ value = 0, onChange }) {
	if (!onChange)
		return (
			<div className="stars">
				<img className="star-icon" src={starIcon} alt="" />
			</div>
		);

	return (
		<div className="stars">
			{[1, 2, 3, 4, 5].map((star) =>
				onChange ? (
					<button
						type="button"
						key={star}
						className={`star-button ${star <= value ? "is-selected" : ""}`}
						onClick={() => onChange(star)}
					>
						★
					</button>
				) : (
					<span
						className={star <= Math.round(value) ? "is-selected" : ""}
						key={star}
					>
						★
					</span>
				),
			)}
		</div>
	);
}
