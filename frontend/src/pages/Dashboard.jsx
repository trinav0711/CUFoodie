import React from "react";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const cards = [
    {label:'Search Restaurants', to:'/restaurants'},
    {label:'Browse Dishes', to:'/dishes'},
    {label:'Reviews', to:'/reviews'},
    {label:'Food Trails', to:'/trails'},
    {label:'Budget-Friendly Picks', to:'/budget'},
    {label:'Profile', to:'/profile'}
  ];

  return (
    <div>
      <h3>Dashboard</h3>
      <div className="card-grid" style={{marginTop:12}}>
        {cards.map(c=> (
          <Link key={c.to} to={c.to} className="card" style={{textDecoration:'none',color:'inherit'}}>
            <div style={{fontSize:16,fontWeight:600}}>{c.label}</div>
            <div className="small" style={{marginTop:8}}>Click to open</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
