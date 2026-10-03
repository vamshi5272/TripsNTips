export const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:5000';
export type Location = {id:string; name:string; city:string; type:string; lat:number; lon:number};
export type Stage = {from:string;to:string;from_name:string;to_name:string;mode:string;label:string;cost:number;duration_min:number;kind:string;data_status:string};
export type Route = {id:string;origin:string;destination:string;nodes:string[];stages:Stage[];cost:number;duration_min:number;duration_hours:number;transfers:number;modes:string[];data_status:string;cost_breakdown:{transport_and_access:number;sightseeing:number;total:number}};
export type OptimizeResult = {feasible:boolean;strategy:string;selected_route_id?:string;routes:Route[];candidates_evaluated:number;data_notice:string;explanation?:string;message?:string;suggestions?:string[]};
export async function getLocations(): Promise<{locations:Location[];notice:string}> {
  const response = await fetch(`${API_BASE}/api/cities`);
  if (!response.ok) throw new Error('Could not load demo locations. Is the backend running?');
  return response.json();
}
export async function optimizeTrip(payload: Record<string, unknown>): Promise<OptimizeResult> {
  const response = await fetch(`${API_BASE}/api/optimize`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Could not optimize this trip.');
  return data;
}
