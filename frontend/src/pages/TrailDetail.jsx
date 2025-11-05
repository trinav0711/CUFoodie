import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function TrailDetail() {
  const { id } = useParams();
  const [trail,setTrail] = useState(null);
  const [stops,setStops] = useState([]);

  useEffect(()=>{ 
    fetch(`/trail_api/${id}`).then(r=>r.json()).then(j=>{ setTrail(j.trail); setStops(j.stops) });// Fetch trail details from Flask API
  }, [id]);

  if(!trail) return <div className="small">Loading…</div>;

  return (
    <div>
      <h3>{trail.name}</h3>
      <div className="card">
        {stops.map(s=>(
          <div key={s.menu_id} style={{padding:'8px 0',borderBottom:'1px solid #f6f6f6'}}>
            <div style={{fontWeight:600}}>{s.restaurant_name} • ${s.price}</div>
            <div className="small">{s.name} — {s.dietary_tags}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
