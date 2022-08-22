import React from "react";
import { Container, Nav, Navbar} from "react-bootstrap";
import { Link } from 'react-router-dom';
import "./style.css"

const Header = () => {
    return (
        <>
            <Navbar bg="primary" variant="dark">
                <Container>
                    <Navbar.Brand href="/">MicroDataMetrics</Navbar.Brand>
                    <Nav className="me-auto">

                        <Link to="/" className="nv-link">Home</Link>
                        <Link to="/settings" className="nv-link">Settings</Link>                                         
                        
                    </Nav>
                </Container>
            </Navbar>
        </>
    )

}

export default Header;