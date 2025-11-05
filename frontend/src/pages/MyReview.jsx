import React, { useState, useEffect } from "react";
import { useAuth } from "../App";

export default function MyReviews() {
  const { user } = useAuth();
  const [data,setData] = useState([]);

  useEffect(()=>{
    if(!user) return;

    // Flask API: return only reviews made by the logged-in user
    fetch('/user_reviews_api?user=' + encodeURIComponent(user))
      .then(r=>r.json())
      .then(j=>setData(j));
  }, [user]);

  return (
    <div>
      <h3>My Reviews</h3>
      <div className="card">
        {data.length === 0 && <div className="small">You haven’t written any reviews yet.</div>}
        {data.map(r=>(
          <div key={r.review_id} style={{padding:'8px 0',borderBottom:'1px solid #f6f6f6'}}>
            <div style={{fontWeight:600}}>{r.restaurant_name} <span className="small">• {r.review_date}</span></div>
            <div className="small">Rating: {r.rating}</div>
            <div style={{marginTop:6}}>{r.comment}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
