import React, { useState, useEffect } from "react";

export default function Budget() {
  const [maxPrice, setMaxPrice] = useState(10);
  const [data, setData] = useState([]);

  async function fetchBudget() {
    const res = await fetch('/api/budget?max_price=' + maxPrice);
    const json = await res.json();
    setData(json);
  }

  useEffect(() => { fetchBudget(); }, []);

  return (
    <div>
      <h3>Budget Picks</h3>
      <div className="card">
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <input className="input" type="number" value={maxPrice} onChange={e => setMaxPrice(e.target.value)} />
          <button className="btn" onClick={fetchBudget}>Show</button>
        </div>

        <div style={{ marginTop: 12 }}>
          <table className="table">
            <thead>
              <tr><th>Dish</th><th>Restaurant</th><th>Price</th></tr>
            </thead>
            <tbody>
              {data.length === 0 && <tr><td colSpan={3} className="small">No dishes available</td></tr>}
              {data.map(d => (
                <tr key={`${d.dish_name}-${d.restaurant_name}`}>
                  <td>{d.dish_name}</td>
                  <td>{d.restaurant_name}</td>
                  <td>${d.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

