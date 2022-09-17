import React from "react";
import { Button, Col, Row } from "react-bootstrap";
import { FiPlus } from "react-icons/fi";
import 'bootstrap/dist/css/bootstrap.min.css';

import FormPreferences from "../../Components/FormPreferencesMetrics";
import ShowPreferences from "../../Components/ShowPreferences";
import ShowPreferencesMerge from "../../Components/PreferencesMerge";


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
                <Row style={{ paddingTop:'20px', paddingBottom:'20px' }}>
                    <Col md={{ span: 4, offset:9}} >
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