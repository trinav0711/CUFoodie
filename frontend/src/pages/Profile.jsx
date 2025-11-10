import React, { useState, useEffect } from "react";
import { useAuth } from "../App";

export default function Profile() {
  const { user } = useAuth();
  const [trails,setTrails] = useState([]);
  const [reviews,setReviews] = useState([]);

  useEffect(()=>{
    if(!user) return;
    //fetch('/my_profile_api?user='+encodeURIComponent(user)) // call Flask API to get user profile data
    fetch(`/api/profile?username=${encodeURIComponent(user)}`)
      	.then(r=>r.json())
      	.then(j=>{ setTrails(j.trails||[]); setReviews(j.reviews||[]) })
  }, [user]);

  return (
    <div>
      <h3>Profile</h3>
      <div className="card">
        <div><b>Username:</b> {user||'Not logged in'}</div>
        <div style={{marginTop:8}}><b>Trails created:</b> {trails.length}</div>
        <div style={{marginTop:8}}><b>Number of reviews:</b> {reviews.length}</div>
      </div>
      <div style={{marginTop:12}} className="card">
        <h4>Your Trails</h4>
        {trails.map(t=> <div key={t.trail_id} className="small">{t.name} • {t.count_items} stops</div>)}
      </div>
    </div>
  );
}
