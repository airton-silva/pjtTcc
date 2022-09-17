import React from "react";
import { Container, Nav, Navbar} from "react-bootstrap";
import { BiHomeHeart } from "react-icons/bi";
import { FiSettings } from "react-icons/fi"
import { GiObservatory } from "react-icons/gi"
import { Link } from 'react-router-dom';
import "./style.css"

const Header = () => {
    return (
        <>
            <Navbar bg="primary" variant="dark">
                <Container>
                    <Navbar.Brand href="/">MicroDataMetrics </Navbar.Brand>
                    <Nav className="me-auto">

                        <Link to="/" className="nv-link">Home <BiHomeHeart/> </Link>
                        <Link to="/monitoring" className="nv-link">Monitorando <GiObservatory/></Link> 
                        <Link to="/settings" className="nv-link">Settings <FiSettings/></Link>                                         
                        
                    </Nav>
                </Container>
            </Navbar>
        </>
    )

}

export default Header;