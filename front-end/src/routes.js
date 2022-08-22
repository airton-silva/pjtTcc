import React from "react";
import {Routes,Route } from "react-router-dom";

import Home from "./Pages/Home";
import Settings from "./Pages/Settings"

const MyRoutes = () => {
    return(

            <Routes>
                <Route path="/"  element = {<Home/>} />
                <Route path="/settings" element = {<Settings/>} />
            </Routes>

    )
 }
 
 export default MyRoutes;