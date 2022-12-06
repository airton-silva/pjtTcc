import React from "react";
import { Card, Form, Row, Col, InputGroup, Button } from "react-bootstrap"
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";

const FormSearchCustom = (prop) => {

    const {show, preferenceId}= prop;
    // console.log(show, preferenceId);

    // const [display, setDisplay] = React.useState(show);
    const [validated, setValidated] = React.useState(false);
    const [name, setName] = React.useState("");
    const [type, setType] = React.useState("");
    const [metric, setMetric] = React.useState("");
    const [namePod, setNamePod] = React.useState("");
    const [valueFailure, setValueFailure] = React.useState("");
    const [periodTime, setPeriodTime] = React.useState("");

    const [types, setTypes] = React.useState([]);
    const [typeMetric, setTypeMetric] = React.useState([]);
    const [pods, setPods] = React.useState([]);
    return (
        <>
            <Form  >
            <Row>
                <Form.Group as={Col} md="12" controlId="validationCustom01">
                    <Form.Label>Buscar</Form.Label>
                    <Form.Control
                        required
                        type="text"
                        name="Buscar"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Falhas de estouro de memória"                    
                    />
                    <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>

            </Row>
            <Row>
                <Form.Group as={Col} md="2" controlId="formBasicSelect">
                            <Form.Label>Operador</Form.Label>
                            <Form.Control
                            as="select"
                            name="metric"
                            value={metric}
                            onChange={e => {
                                setMetric(e.target.value);
                            }}
                            >
                                <option value="none">none</option>
                                <option value="query">query</option>
                                <option value="query_rate">query_rate</option>

                            </Form.Control>
                </Form.Group>
                <Form.Group as={Col} md="5" controlId="validationCustom02">
                    <Form.Label>Metrica</Form.Label>
                    <Form.Control
                    as="select"
                    name="type"
                    value={type}
                    onChange={e => {
                    setType(e.target.value);
                    }}
                    >
                        
                        { 
                        typeMetric.map((type,i)=>
                        <option key={i} value={type}>{type}</option>)                                        
                            
                        }
                        

                    </Form.Control>
                    <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                </Form.Group>

                <Form.Group as={Col} md="1" controlId="formBasicSelect">
                            <Form.Label>Operador</Form.Label>
                            <Form.Control
                            as="select"
                            name="metric"
                            value={metric}
                            onChange={e => {
                                setMetric(e.target.value);
                            }}
                            >
                                <option value="=">=</option>
                                <option value="!=">!=</option>
                                <option value="=~">=~</option>
                                <option value="!~">!~</option>
                            </Form.Control>
                </Form.Group>

                <Form.Group as={Col} md="4" controlId="formBasicSelect">
                    <Form.Label>Serviço a ser Monitorado</Form.Label>
                    <Form.Control
                    as="select"
                    name="namePod"
                    value={namePod}

                    onChange={e => {
                        setNamePod(e.target.value);
                    }}
                    >                                                                                
                        { 
                        pods.map((pod,i)=>
                        <option key={i} value={pod.metric.pod}>{pod.metric.pod}</option>)                                        
                            
                        }
                        

                    </Form.Control>
                </Form.Group>
            </Row>


            </Form>


        </>
    )
}

export default FormSearchCustom;