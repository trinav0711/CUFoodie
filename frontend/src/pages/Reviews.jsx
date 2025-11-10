import React, { useState, useEffect } from "react";
import { useAuth } from "../App";

export default function Reviews() {
  const [recent,setRecent] = useState([]);
  const [mine,setMine] = useState([]);
  const { user } = useAuth();

  useEffect(()=>{
    // Flask API: recent public reviews
    fetch('/reviews_api') // <-- Flask endpoint
      .then(r=>r.json())
      .then(j=>setRecent(j));

    if(user){
      // Flask API: reviews only by this user
      fetch('/api/reviews/user?user=' + encodeURIComponent(user))
        .then(r=>r.json())
        .then(j=>setMine(j));
    }
  }, [user]);

  return (
    <div>
      <h3>Reviews</h3>

      {/* My Reviews */}
      {user && (
        <div className="card" style={{marginBottom:16}}>
          <h4>My Reviews</h4>
          {mine.length === 0 && <div className="small">You haven’t reviewed anything yet.</div>}
          {mine.map(r=>(
            <div key={r.review_id} style={{padding:'8px 0',borderBottom:'1px solid #f6f6f6'}}>
              <div style={{fontWeight:600}}>{r.restaurant_name} <span className="small">• {r.review_date}</span></div>
              <div className="small">Rating: {r.rating}</div>
              <div style={{marginTop:6}}>{r.comment}</div>
            </div>
          ))}
        </div>
      )}

      {/* Recent Community Reviews */}
      <div className="card">
        <h4>Recent Reviews From Community</h4>
        {recent.map(r=>(
          <div key={r.review_id} style={{padding:'8px 0',borderBottom:'1px solid #f6f6f6'}}>
            <div style={{fontWeight:600}}>{r.user_name} <span className="small">• {r.review_date}</span></div>
            <div className="small">{r.restaurant_name} — Rating: {r.rating}</div>
            <div style={{marginTop:6}}>{r.comment}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
