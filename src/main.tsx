import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Compass, Menu, X, Bookmark, MapPin, ArrowRight } from 'lucide-react';
import Home from './pages/Home';
import Planner from './pages/Planner';
import Results from './pages/Results';
import SavedTrips from './pages/SavedTrips';
import HowItWorks from './pages/HowItWorks';
import About from './pages/About';
import type { Location, OptimizeResult } from './services/api';
import './styles.css';

function App(){
 const [page,setPage]=useState('home');const [mobileOpen,setMobileOpen]=useState(false);const [result,setResult]=useState<OptimizeResult|null>(null);const [locations,setLocations]=useState<Location[]>([]);const [input,setInput]=useState<Record<string,unknown>>({});
 const go=(p:string)=>{setPage(p);setMobileOpen(false);window.scrollTo({top:0,behavior:'smooth'});};
 const nav=[['Home','home'],['Plan a Trip','plan'],['How It Works','how'],['About','about']];
 return <div className="app-shell"><header className="topbar"><button className="brand" onClick={()=>go('home')}><span className="brand-mark"><Compass size={22}/></span><span>Trips<span className="brand-accent">N</span>Tips<small>PLAN SMARTER. TRAVEL BETTER.</small></span></button><nav className={mobileOpen?'nav nav-open':'nav'}>{nav.map(([label,p])=><button key={p} className={page===p?'nav-link nav-active':'nav-link'} onClick={()=>go(p)}>{label}</button>)}<button className="nav-link saved-nav" onClick={()=>go('saved')}><Bookmark size={15}/> Saved Trips</button><button className="button button-primary nav-cta" onClick={()=>go('plan')}>Plan my trip <ArrowRight size={15}/></button></nav><button className="mobile-menu" onClick={()=>setMobileOpen(v=>!v)} aria-label="Toggle navigation">{mobileOpen?<X/>:<Menu/>}</button></header>
 <main>{page==='home'&&<Home onPlan={()=>go('plan')}/ >}{page==='plan'&&<Planner onResults={(r,l,i)=>{setResult(r);setLocations(l);setInput(i);go('results');}}/>}{page==='results'&&result&&<Results result={result} locations={locations} input={input} onBack={()=>go('plan')}/ >}{page==='results'&&!result&&<div className="empty-state"><h2>No search results yet</h2><button className="button button-primary" onClick={()=>go('plan')}>Plan a trip</button></div>}{page==='saved'&&<SavedTrips/>}{page==='how'&&<HowItWorks/>}{page==='about'&&<About/>}</main>
 <footer className="footer"><div className="footer-brand"><span className="brand-mark"><Compass size={20}/></span><div><b>TripsNTips</b><p>PLAN SMARTER • TRAVEL BETTER • EXPLORE MORE</p></div></div><div className="footer-note"><MapPin size={15}/> Hackathon prototype · Demo data only · No ticket booking</div><p className="copyright">© {new Date().getFullYear()} TripsNTips. Sample prices and schedules are illustrative.</p></footer></div>
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
