import { formatNumber } from "../../utils/format";

import windIcon from "../../assets/icons/wind.svg";
import directionIcon from "../../assets/icons/direction.svg";
import waveIcon from "../../assets/icons/wave.svg";
import waterTemperatureIcon from "../../assets/icons/water-temperature.svg";
import airTemperatureIcon from "../../assets/icons/air-temperature.svg";
import cloudIcon from "../../assets/icons/cloud.svg";

const weatherItems = [
	["wind_speed", windIcon, "Wind Speed", "m/s"],
	["wind_direction", directionIcon, "Wind Direction", "°"],
	["wave_height", waveIcon, "Wave Height", "m"],
	["water_temperature", waterTemperatureIcon, "Water Temp", "°C"],
	["air_temperature", airTemperatureIcon, "Air Temp", "°C"],
	["cloud_cover", cloudIcon, "Cloud Cover", "%"],
];

export default function WeatherGrid({ weather, compact = false }) {
	if (!weather) return <p className="empty-message">Current weather is unavailable.</p>;

	return (
		<div className={`weather-grid ${compact ? "weather-grid--compact" : ""}`}>
			{weatherItems.map(([key, icon, label, unit]) => (
				<div className="weather-item" key={key}>
					<img className="weather-icon" src={icon} alt="" />

					<strong>{formatNumber(weather[key])}</strong>

					<span className="weather-unit">{unit}</span>

					{!compact && <span className="weather-label">{label}</span>}
				</div>
			))}
		</div>
	);
}
