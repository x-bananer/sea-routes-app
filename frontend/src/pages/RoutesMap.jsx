import RouteMap from "../components/Map/RouteMap";
import chevronIcon from "../assets/icons/chevron.svg";

const colors = ["#087fc6", "#13a354", "#793bbd"];

export default function RoutesMap({ routes, onSelect }) {
	return (
		<main className="map-screen">
			<header className="app-header">
				<h1>SeaRoutes</h1>
			</header>
			<RouteMap routes={routes} onSelect={onSelect} />
			<section className="route-sheet">
				<h2 id="routes-heading">Routes</h2>
				<ul className="route-list">
					{routes.map((route, index) => (
						<li key={route.route_id}>
							<button onClick={() => onSelect(route)}>
								<span
									className="route-dot"
									style={{ background: colors[index % colors.length] }}
								/>
								{route.name}
								<img className="route-chevron" src={chevronIcon} alt="" />
							</button>
						</li>
					))}
				</ul>
			</section>
		</main>
	);
}
