import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

export default function Trails() {
  const [type, setType] = useState('');
  const [data, setData] = useState([]);

  async function fetchData() {
    let url = "/api/trails";
    if (type.trim()) {
      url = `/api/trails/name/${encodeURIComponent(type)}`;
    }

    try {
      const res = await fetch(url);
      const rows = await res.json();

      // Map backend fields for consistent display
      const mapped = rows.map(t => ({
        trail_id: t.trail_id,
        name: t.trail_name,   // backend returns trail_name
        user_name: t.user_name,
        count_items: t.count_items || 0
      }));

      setData(mapped);
    } catch (e) {
      console.error("Error fetching trails:", e);
      setData([]);
    }
  }

  useEffect(() => { fetchData(); }, []);

  return (
    <div>
      <h3>Food Trails</h3>
      <div className="card">
        <div className="controls">
          <input
            className="input"
            placeholder="Trail type"
            value={type}
            onChange={e => setType(e.target.value)}
          />
          <button className="btn" onClick={fetchData}>Apply</button>
        </div>

        {data.length === 0 && <div className="small">No trails found</div>}
        {data.map(t => (
          <div key={t.trail_id} className="card" style={{ marginTop: 8 }}>
            <div style={{ fontWeight: 700 }}>{t.name}</div>
            <div className="small">by {t.user_name} • {t.count_items} stops</div>
            <div style={{ marginTop: 8 }}>
              <Link to={`/trail/${t.trail_id}`} className="link">View Trail</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

