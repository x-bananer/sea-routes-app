import { useEffect, useState } from "react";
import { getRouteDetails, getRoutes, saveRating } from "./api";
import RoutesMap from "./pages/RoutesMap";
import RouteDetails from "./pages/RouteDetails";
import RateRoute from "./pages/RateRoute";

export default function App() {
	const [routeDetails, setRouteDetails] = useState(null);
	const [routes, setRoutes] = useState([]);
	const [routesError, setRoutesError] = useState("");
	const [routesLoading, setRoutesLoading] = useState(true);
	const [screen, setScreen] = useState("map");
	const [modalOpen, setModalOpen] = useState(false);
	const [notice, setNotice] = useState("");
	
	useEffect(() => {
		let cancelled = false;

		getRoutes()
			.then((loadedRoutes) => {
				if (!cancelled) {
					setRoutes(loadedRoutes);
				}
			})
			.catch((error) => {
				if (!cancelled) {
					setRoutesError(error.message);
				}
			})
			.finally(() => {
				if (!cancelled) {
					setRoutesLoading(false);
				}
			});

		return () => {
			cancelled = true;
		};
	}, []);

	useEffect(() => {
		if (!notice) {
			return undefined;
		}
		const timeout = window.setTimeout(() => setNotice(""), 3000);
		return () => window.clearTimeout(timeout);
	}, [notice]);

	const selectRoute = async (route) => {
		setRouteDetails(route);
		setScreen("details");
		setNotice("Loading route details…");

		try {
			const details = await getRouteDetails(route.id);
			setRouteDetails(details);
			setNotice("");
		} catch (error) {
			setNotice(error.message || "Route details could not be loaded.");
		}
	};

	const handleRating = async (rating) => {
		await saveRating(routeDetails.id, rating);
		setModalOpen(false);
		setNotice("Rating submitted. Statistics will update shortly.");
	};

	return (
		<>
			{screen === "map" && routesLoading && <p className="toast">Loading routes…</p>}
			{screen === "map" && routesError && <p className="toast">{routesError}</p>}
			{screen === "map" && !routesLoading && !routesError && (
				<RoutesMap routes={routes} onSelect={selectRoute} />
			)}
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
