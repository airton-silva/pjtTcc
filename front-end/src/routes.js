import React from "react";
import {Routes,Route } from "react-router-dom";

import Home from "./Pages/Home";
import Settings from "./Pages/Settings";
import Monitoring from "./Pages/Monitoring";
import SearchMetrics from "./Pages/Search";

const MyRoutes = () => {
    return(

            <Routes>
                <Route path="/"  element = {<Home/>} />
                <Route path="/search"  element = {<SearchMetrics/>} />
                <Route path="/monitoring" element = {<Monitoring/>} />
                <Route path="/settings" element = {<Settings/>} />
            </Routes>

    )
 }
 
 export default MyRoutes;