import React from "react";
import Routes from "./routes";
import { BrowserRouter} from "react-router-dom"
import {Container} from "react-bootstrap"

import Header from "./Components/Header";

function App() {
  return (
    <BrowserRouter >
        <div className="App">
          <Header />
            <Container>              
              <Routes />
            </Container>
        </div>
    </BrowserRouter>    

  );
}

export default App;
