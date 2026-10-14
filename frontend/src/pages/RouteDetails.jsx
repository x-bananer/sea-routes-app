import RouteMap from "../components/Map/RouteMap";
import WeatherGrid from "../components/Weather/WeatherGrid";
import Stars from "../components/Rating/Stars";
import starIcon from "../assets/icons/star.svg";
import usersIcon from "../assets/icons/users.svg";

export default function RouteDetails({ route, onBack, onRate }) {
	const groups = route.ratings_across_conditions || [];
	return (
		<main className="details-screen">
			<header className="details-header">
				<button className="back-button" onClick={onBack}>
					‹
				</button>
				<h1>{route.name}</h1>
			</header>
			<RouteMap routes={[route]} selectedRoute={route} compact />
			<section className="details-content">
				<div className="title-row">
					<h2>{route.name}</h2>
					<button
						className="primary-button primary-button--small"
						onClick={onRate}
					>
						Rate Route
					</button>
				</div>
				<section className="weather-card">
					<h3>Current Weather</h3>
					<WeatherGrid weather={route.current_weather} />
				</section>
				<section className="suitability-card">
					<span>Suitability</span>
					<strong>
						{route.suitability == null
							? "Not enough data"
							: `${route.suitability.toFixed(1)}/5`}
					</strong>
				</section>
				<div className="summary-grid">
					<section className="summary-card">
						<Stars value={route.overall_rating || 0} />
						<strong>{route.overall_rating?.toFixed(1) || "—"}</strong>
						<span>Average rating</span>
					</section>
					<section className="summary-card">
						<img className="people-icon" src={usersIcon} alt="" />
						<strong>{route.total_ratings ?? 0}</strong>
						<span>Total ratings</span>
					</section>
				</div>
				<section className="conditions-section">
					<h3>Ratings Across Conditions</h3>
					{groups.length ? (
						groups.map((group, index) => (
							<article className="condition-card" key={index}>
								<div className="condition-rating">
									<img className="condition-star" src={starIcon} alt="" />
									<strong>{group.average_rating.toFixed(1)}</strong>
									<small>
										{group.total_ratings}{" "}
										{group.total_ratings === 1 ? "rating" : "ratings"}
									</small>
								</div>
								<WeatherGrid weather={group.weather} compact />
							</article>
						))
					) : (
						<p className="empty-message">No ratings yet.</p>
					)}
				</section>
			</section>
		</main>
	);
}
