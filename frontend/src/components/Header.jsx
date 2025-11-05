import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../App";

export default function Header() {
  const { user } = useAuth();
  const navigate = useNavigate();
  return (
    <div className="header">
      <div className="brand">CUFoodie</div>
      <div className="nav">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/restaurants">Restaurants</Link>
        <Link to="/dishes">Dishes</Link>
        <Link to="/trails">Trails</Link>
        <Link to="/budget">Budget</Link>
        <Link to="/profile">Profile</Link>
        <Link to="/reviews">Reviews</Link>
        {user ? (
          <span style={{marginLeft:12}} className="small">Logged in as {user}</span>
        ) : (
          <span style={{marginLeft:12}} className="small link" onClick={()=>navigate('/')}>Login</span>
        )}
      </div>
    </div>
  );
}
