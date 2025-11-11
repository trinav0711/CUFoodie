import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function TrailDetail() {
  const { id } = useParams();
  const [trail, setTrail] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/trails/${id}`)
      .then(r => r.json())
      .then(rows => {
        setTrail(rows);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="small">Loading…</div>;
  if (!trail || trail.length === 0) return <div className="small">Trail not found</div>;

  return (
    <div>
      <h3>{trail[0].trail_name}</h3>
      <div className="card small" style={{marginBottom:12}}>
        Created by <b>{trail[0].user_name}</b><br/>
        Total stops: {trail.length}
      </div>
      {trail.map((t, idx) => (
        <div key={idx} className="card small" style={{marginBottom:8}}>
          <b>Stop {idx + 1}</b>: {t.dish_name} at {t.restaurant_name} — ${t.price} ({t.location})
        </div>
      ))}
    </div>
  );
}

