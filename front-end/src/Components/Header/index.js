import React from "react";
import { CloseButton, Container, Modal, Nav, Navbar } from "react-bootstrap";
import { BiHomeHeart } from "react-icons/bi";
import { FiSettings } from "react-icons/fi"
import { GiObservatory } from "react-icons/gi"
import { FiSearch } from "react-icons/fi"
import { IoMdNotifications } from "react-icons/io"
import { Link } from 'react-router-dom';
import api from "../../Services/Api"
import _ from "lodash";
import "./style.css"
import Formats from "../../Utils/Formats";

const Header = () => {

    const [alerts, setAlerts] = React.useState([])
    const [lgShow, setLgShow] = React.useState(false);

    const getAlets = async () => {
        try {
            const resp = await api.get('/alerts/all');
            const { data } = resp
            setAlerts(data)
        } catch (error) {
            console.error(error);
        }

    };

    console.log(alerts)
    React.useEffect(() => {
        getAlets();


    }, []);
    return (
        <>
            <Navbar bg="primary" variant="dark">
                <Container>
                    <Navbar.Brand href="/">MicroDataMetrics </Navbar.Brand>
                    <Nav className="me-auto">

                        <Link to="/" className="nv-link"><BiHomeHeart /> Cluster </Link>
                        <Link to="/search" className="nv-link"><FiSearch /> Consultas </Link>
                        <Link to="/monitoring" className="nv-link"><GiObservatory /> Apps Monitorados </Link>
                        <Link to="/settings" className="nv-link"><FiSettings /> Config </Link>

                    </Nav>
                    {alerts.length > 0 && (
                        <IoMdNotifications color="#F4795F" size={"25px"} onClick={() => setLgShow(true)} title="Alerts" />
                    )}
                </Container>
            </Navbar>


            <Modal
                size="lg"
                show={lgShow}
                onHide={() => setLgShow(false)}
                aria-labelledby="example-modal-sizes-title-lg"
            >
                <Modal.Header>

                    <Modal.Title id="example-modal-sizes-title-lg">
                        Alertas de provaveis falhas <CloseButton className="close" onClick={() => setLgShow(false)} />
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <ul>

                        {alerts.length > 0 && (
                            alerts.map((val, key) => {
                                console.log(val.type)
                                return (
                                    <li className="alert alert-danger">
                                        <span><strong>Pod:</strong> {val.pod} </span>
                                        <span style={{ marginLeft:'30px' }}><strong>Data:</strong> {val.create_at}</span><br/>
                                        <span ><strong>Metrica:</strong> {val.type}</span>
                                        <span style={{ marginLeft:'10px' }}><strong>Tipo:</strong> {val.mtype}</span>
                                        <span style={{ marginLeft:'10px' }}><strong>tempo:</strong> {Formats.formTimeStampToHours(val.time)}</span>
                                        <span style={{ marginLeft:'10px' }}><strong>valor:</strong> {val.value}</span>
                                    </li>
                                    
                                )

                            })
                        )}

                    </ul>

                </Modal.Body>
            </Modal>
        </>
    )

}

export default Header;