import React, { useState, useEffect } from "react";

export default function Budget() {
  const [maxPrice,setMaxPrice] = useState(10);
  const [data,setData] = useState([]);

  async function fetchBudget() {
    const res = await fetch('/budget_api?maxPrice='+maxPrice);
    setData(await res.json());
  }

  useEffect(()=>{ fetchBudget(); }, []);

  return (
    <div>
      <h3>Budget Picks</h3>
      <div className="card">
        <div style={{display:'flex',gap:8,alignItems:'center'}}>
          <input className="input" type="number" value={maxPrice} onChange={e=>setMaxPrice(e.target.value)} />
          <button className="btn" onClick={fetchBudget}>Show</button>
        </div>
        <div style={{marginTop:12}}>
          <table className="table"><thead><tr><th>Dish</th><th>Restaurant</th><th>Price</th></tr></thead>
          <tbody>
            {data.map(d=>(
              <tr key={d.menu_id}><td>{d.name}</td><td>{d.restaurant_name}</td><td>${d.price}</td></tr>
            ))}
          </tbody></table>
        </div>
      </div>
    </div>
  );
}
