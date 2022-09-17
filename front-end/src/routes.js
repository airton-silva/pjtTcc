import React from "react";
import {Routes,Route } from "react-router-dom";

import Home from "./Pages/Home";
import Settings from "./Pages/Settings";
import Monitoring from "./Pages/Monitoring";

const MyRoutes = () => {
    return(

            <Routes>
                <Route path="/"  element = {<Home/>} />
                <Route path="/monitoring" element = {<Monitoring/>} />
                <Route path="/settings" element = {<Settings/>} />
            </Routes>

    )
 }
 
 export default MyRoutes;