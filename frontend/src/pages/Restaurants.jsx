import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

export default function Restaurants() {
  const [query, setQuery] = useState('');       // Search by restaurant name
  const [location, setLocation] = useState(''); // Filter by neighborhood/location
  const [cuisine, setCuisine] = useState('');   // Filter by cuisine type
  const [minRating, setMinRating] = useState('');// Filter by minimum rating
  const [data, setData] = useState([]);         // Stores list of restaurants returned from Flask API

  async function fetchList() {
    try {
      // Flask API call
      const q = new URLSearchParams({name: query, location, cuisine, minRating}).toString();
      const res = await fetch('/restaurants_api?' + q); // <-- call Flask API here
      const json = await res.json();                    
      setData(json);                                    
    } catch(e) {
      console.error(e);                                 
    }
  }

  // Load all restaurants initially (without filters)
  useEffect(() => { fetchList(); }, []);

  return (
    <div>
      <h3>Restaurants</h3>
      <div className="card">
        <div className="controls">
          {/* Input fields for filtering */}
          <input className="input" placeholder="Search name" value={query} onChange={e => setQuery(e.target.value)} />
          <input className="input" placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} />
          <input className="input" placeholder="Cuisine" value={cuisine} onChange={e => setCuisine(e.target.value)} />
          <input className="input" placeholder="Min rating" value={minRating} onChange={e => setMinRating(e.target.value)} style={{width: 120}} />
          <button className="btn" onClick={fetchList}>Apply</button>
        </div>

        <table className="table" style={{marginTop: 12}}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Cuisine</th>
              <th>Location</th>
              <th>Avg Rating</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {data.length === 0 && 
              <tr>
                <td colSpan={5} className="small">No restaurants found — press Apply</td>
              </tr>
            }
            {/* Map each restaurant returned by Flask API */}
            {data.map(r => (
              <tr key={r.restaurant_id}>
                <td>{r.name}</td>
                <td>{r.cuisine_type}</td>
                <td className="small">{r.location}</td>
                <td>{r.avg_rating || '—'}</td>
                {/* Link to restaurant details page */}
                <td><Link to={`/restaurant/${r.restaurant_id}`} className="link">View Menu</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
