import React, { useState, createContext, useContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Context
export const AuthContext = createContext();
export function useAuth(){ return useContext(AuthContext); }

// Components
import Header from "./components/Header";

// Pages
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import Restaurants from "./pages/Restaurants";
import RestaurantDetail from "./pages/RestaurantDetail";
import Dishes from "./pages/Dishes";
import Trails from "./pages/Trails";
import TrailDetail from "./pages/TrailDetail";
import Reviews from "./pages/Reviews";
import Budget from "./pages/Budget";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";

export default function App() {
  const [user, setUser] = useState(null);

  return (
    <AuthContext.Provider value={{user,setUser}}>
      <BrowserRouter>
        <div className="app">
          <Header />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/restaurants" element={<Restaurants />} />
            <Route path="/restaurant/:id" element={<RestaurantDetail />} />
            <Route path="/dishes" element={<Dishes />} />
            <Route path="/trails" element={<Trails />} />
            <Route path="/trail/:id" element={<TrailDetail />} />
            <Route path="/reviews" element={<Reviews />} />
            <Route path="/budget" element={<Budget />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}
