import { Clock3, IndianRupee, MapPin, ArrowRight, Bookmark } from 'lucide-react';
import type { Route } from '../services/api';
export default function RouteCard({route,selected,onSelect,onSave}:{route:Route;selected:boolean;onSelect:()=>void;onSave:()=>void}) {
  const title = route.id === 'route-1' ? 'Pocket Saver candidate' : route.id === 'route-2' ? 'Time Saver candidate' : 'Smart alternative';
  return <article className={`route-card ${selected?'selected':''}`}>
    <div className="route-card-top"><span className="eyebrow">{title}</span><button className="icon-button" title="Save journey" onClick={onSave}><Bookmark size={17}/></button></div>
    <div className="metrics"><div><IndianRupee size={17}/><strong>₹{Math.round(route.cost).toLocaleString('en-IN')}</strong><small>demo total</small></div><div><Clock3 size={17}/><strong>{route.duration_hours} h</strong><small>elapsed time</small></div><div><MapPin size={17}/><strong>{route.transfers}</strong><small>connections</small></div></div>
    <div className="mode-list">{route.modes.map(m=><span key={m} className="pill">{m}</span>)}</div>
    <p className="route-sub">{route.stages.length} journey stages · Demo values only</p>
    <div className="route-actions"><button className="button button-outline" onClick={onSelect}>View on map</button><button className="button button-primary" onClick={onSelect}>View itinerary <ArrowRight size={16}/></button></div>
  </article>;
}
