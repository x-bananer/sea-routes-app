import { Fragment, useEffect } from "react";
import {
	CircleMarker,
	MapContainer,
	Polyline,
	TileLayer,
	Tooltip,
	useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

const colors = ["#087fc6", "#13a354", "#793bbd"];

function FitRoute({ route }) {
	const map = useMap();
	
	useEffect(() => {
		if (route?.coordinates?.length)
			map.fitBounds(route.coordinates, { padding: [24, 24], maxZoom: 14 });
	}, [map, route]);

	return null;
}

export default function RouteMap({
	routes,
	selectedRoute,
	onSelect,
	compact = false,
}) {
	return (
		<MapContainer
			center={[60.1699, 24.9384]}
			zoom={12}
			className={`route-map ${compact ? "route-map--compact" : ""}`}
			scrollWheelZoom
		>
			<TileLayer
				attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
				url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			/>
			{routes.map((route, index) => {
				const selected = route.route_id === selectedRoute?.route_id;
				return (
					<Fragment key={route.route_id}>
						<Polyline
							positions={route.coordinates}
							pathOptions={{
								color: colors[index % colors.length],
								weight: selected ? 6 : 4,
								opacity: selected ? 1 : 0.88,
							}}
							eventHandlers={{ click: () => onSelect?.(route) }}
						>
							{!compact && (
								<Tooltip permanent direction="top" offset={[0, -8]}>
									{route.name}
								</Tooltip>
							)}
						</Polyline>
						{route.coordinates.map((position, pointIndex) => (
							<CircleMarker
								key={`${route.route_id}-${pointIndex}`}
								center={position}
								radius={selected ? 7 : 6}
								pathOptions={{
									color: "#ffffff",
									fillColor: colors[index % colors.length],
									fillOpacity: 1,
									weight: 2,
								}}
								eventHandlers={{ click: () => onSelect?.(route) }}
							/>
						))}
					</Fragment>
				);
			})}
			{selectedRoute && <FitRoute route={selectedRoute} />}
		</MapContainer>
	);
}
