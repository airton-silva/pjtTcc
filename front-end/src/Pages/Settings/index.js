import React from "react";
import { Button, Col, Row } from "react-bootstrap";
import { FiPlus } from "react-icons/fi";
import 'bootstrap/dist/css/bootstrap.min.css';

import FormPreferences from "../../Components/FormPreferencesMetrics";
import ShowPreferences from "../../Components/ShowPreferences";
import DataSources from "../../Components/DataSources";


const Settings = () => {

    const [openForm, setOpenForm] = React.useState("none");

    const handleForm = () => {
       
       if(openForm === "none") {
           setOpenForm("block");
       }else
           setOpenForm("none");
    }

    return (
        <>

            <div style={{ marginTop: '20px', boxShadow: '0 4px 8px 0 rgba(97, 94, 94, 0.2), 0 6px 20px 0 rgba(22, 21, 21, 0.19)', border: 'none' }}>

                <div>
                    <DataSources />
                </div>    
                <Row style={{ paddingTop:'20px', paddingBottom:'20px' }}>
                    <Col md={{ span: 7, offset:1}} >
                        <h4>Criar predefinição de parametros de Falha</h4>
                    </Col>
                    <Col md={{ span: 3, offset:1}} >
                        <Button onClick={handleForm} ><FiPlus/> Criar Prefrerencias  </Button>
                    </Col>
                </Row>
                <div>
                    <FormPreferences show={openForm}/>
                </div>
                <div>
                    <ShowPreferences />
                </div>
              

            </div>

        </>
    )

}

export default Settings;