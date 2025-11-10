import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function TrailDetail() {
  const { id } = useParams();
  const [trail, setTrail] = useState(null);

  useEffect(() => {
    fetch(`/api/trails`)
      .then(r => r.json())
      .then(rows => {
        const t = rows.find(x => String(x.trail_id) === String(id));
        setTrail(t || null);
      });
  }, [id]);

  if (!trail) return <div className="small">Loading…</div>;

  return (
    <div>
      <h3>{trail.name}</h3>
      <div className="card small">
        Created by <b>{trail.user_name}</b><br/>
        Contains {trail.count_items} stops
      </div>
    </div>
  );
}
