import { useEffect, useState } from "react";
import routes from "./data/routes.json";
import RoutesMap from "./pages/RoutesMap";
import RouteDetails from "./pages/RouteDetails";
import RateRoute from "./pages/RateRoute";

export default function App() {
	const [routeDetails, setRouteDetails] = useState(null);
	const [screen, setScreen] = useState("map");
	const [modalOpen, setModalOpen] = useState(false);
	const [notice, setNotice] = useState("");
	
	useEffect(() => {
		if (!notice) {
			return undefined;
		}
		const timeout = window.setTimeout(() => setNotice(""), 3000);
		return () => window.clearTimeout(timeout);
	}, [notice]);

	const selectRoute = (route) => {
		setRouteDetails(route);
		setScreen("details");
	};

	const handleRating = (rating) => {
		setRouteDetails({
			...routeDetails,
			total_ratings: routeDetails.total_ratings + 1,
			overall_rating: routeDetails.overall_rating || rating.rating,
		});
		setModalOpen(false);
		setNotice("Rating submitted");
	};

	return (
		<>
			{screen === "map" && <RoutesMap routes={routes} onSelect={selectRoute} />}
			{screen === "details" && routeDetails && (
				<RouteDetails
					route={routeDetails}
					onBack={() => {
						setScreen("map");
						setNotice("");
					}}
					onRate={() => setModalOpen(true)}
				/>
			)}
			{notice && <p className="toast">{notice}</p>}
			{modalOpen && (
				<RateRoute
					route={routeDetails}
					onClose={() => setModalOpen(false)}
					onSubmit={handleRating}
				/>
			)}
		</>
	);
}
