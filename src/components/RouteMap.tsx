import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import { useEffect } from 'react';
import type { Location, Route } from '../services/api';
import 'leaflet/dist/leaflet.css';

// Fix marker assets when bundled by Vite.
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
L.Icon.Default.mergeOptions({iconRetinaUrl:markerIcon2x, iconUrl:markerIcon, shadowUrl:markerShadow});

function FitBounds({locations}:{locations:Location[]}) {
  const map = useMap();
  useEffect(() => { if (locations.length) map.fitBounds(locations.map(p => [p.lat,p.lon] as [number,number]), {padding:[30,30]}); }, [locations,map]);
  return null;
}

const routeColors = ['#2563eb','#e76f51','#16a34a','#9333ea','#d97706'];
export default function RouteMap({locations,routes,selectedId,onSelect}:{locations:Location[];routes:Route[];selectedId?:string;onSelect:(id:string)=>void}) {
  const byId = new Map(locations.map(p => [p.id,p]));
  const selected = routes.find(r => r.id === selectedId);
  const displayed = selected ? [selected] : routes.slice(0,3);
  const visibleIds = new Set(displayed.flatMap(r => r.nodes));
  const visibleLocations = locations.filter(p => visibleIds.has(p.id));
  return <div className="map-wrap"><MapContainer center={[16.5,77.5]} zoom={5} scrollWheelZoom className="map">
    <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
    {visibleLocations.map(p => <Marker key={p.id} position={[p.lat,p.lon]}><Popup><b>{p.name}</b><br/>{p.type.replaceAll('_',' ')}</Popup></Marker>)}
    {displayed.map((r,i) => { const pts = r.nodes.map(id => byId.get(id)).filter(Boolean) as Location[]; return pts.length > 1 ? <Polyline key={r.id} positions={pts.map(p => [p.lat,p.lon] as [number,number])} pathOptions={{color:routeColors[i%routeColors.length],weight:r.id===selectedId?6:4,opacity:r.id===selectedId?0.95:0.65}} eventHandlers={{click:()=>onSelect(r.id)}} /> : null; })}
    <FitBounds locations={visibleLocations}/>
  </MapContainer><div className="map-note">Conceptual connections from demo data. Lines are not verified road or rail geometry.</div></div>;
}
