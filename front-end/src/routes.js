import React from "react";
import {Routes,Route } from "react-router-dom";

import Home from "./Pages/Home";
import Settings from "./Pages/Settings"

const MyRoutes = () => {
    return(

            <Routes>
                <Route element = { <Home/> }  path="/" />
                <Route element = { <Settings/> }  path="/settings" />
            </Routes>

    )
 }
 
 export default MyRoutes;