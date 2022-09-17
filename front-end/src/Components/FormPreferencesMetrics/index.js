import React from "react";
import { Card, Form, Row, Col, InputGroup, Button } from "react-bootstrap"
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";

const FormPreferences = (prop) => {

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
    
    const createPreferences = async (event) => {
        event.preventDefault();

        var now = Formats.formatTimesStampToDateTimeEUA(Date.now());
        const data = {
            "name":name,
            "name_pod": namePod,
            "metric": metric,
            "type": type,
            "value_failure": valueFailure,
            "period_time": periodTime,
            "create_at": now,
            "update_at":now,
    
        };


        try {
            const resp = await api.post('/preferences', data);
            alert("Definição de Preferencias de "+ resp.data.name+ "\nRealizada com sucesso");
            show = "none";

        } catch (error) {
            console.log(error);
            
        }


    }

    const getTypesMetrics = async () => {
        
        try {
            const resp = await api.get('/metadata');
            const response = resp.data.data;
            setTypes(Object.keys(response));
            setTypeMetric(Object.keys(response));
                        
        } catch (error) {
            console.log(error);
            
        }
    }

    const getPods = async () => {
        try {

            const resp = await api.get('/pods');
            const response = resp.data.data.result; 
            setPods(response);
                        
        } catch (error) {
            console.log(error);
            
        }
    }

    const getDefinitionFail = async (id) => {

        try {

            const resp = await api.get(`preferences/${id}`);
            const response = resp.data; 
            
            setName(response.name);
            setMetric(response.metric);            
            setNamePod(response.name_pod);
            setType(response.type);
            setValueFailure(response.value_failure);
            setPeriodTime(response.period_time);


                            
        } catch (error) {
            console.log(error);
            
        }

    }

    const updatePreferences = async (event) => {
        event.preventDefault();

        var now = Formats.formatTimesStampToDateTimeEUA(Date.now());
        const data = {
            "name":name,
            "name_pod": namePod,
            "metric": metric,
            "type": type,
            "value_failure": valueFailure,
            "period_time": periodTime,
            "create_at": now,
            "update_at":now,
    
        };


        try {
            const resp = await api.put(`/preferences/${preferenceId}`, data);
            alert("Atualização de Preferencias id = "+ resp.data.id+ "\nRealizada com sucesso");
            show = "none";

        } catch (error) {
            console.log(error);
            
        }


    }
    // console.log(definitionFail);
    const handleSubmit = (event) => {    
      event.preventDefault();
      const form = event.currentTarget;
      console.log(form.checkValidity());
       
      if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
            return false;
      }
      setValidated(true);
      createPreferences();
    
       
    };

    const saveOrUpdate = (e) =>{
        if(show === null && preferenceId > 0){
            updatePreferences(e);
        }else{
            createPreferences(e);
        }
    }

    React.useEffect(() => {
        getTypesMetrics();
        getPods();
        if(show === null && preferenceId > 0){
            getDefinitionFail(preferenceId);
        }
       
        // setValidated(true);

    }, []);

    return (
        <>
            <div style={{ display: show }}>
                <Card className="text-center">
                    <Card.Header as="h4">Cadastro de padrões considerados como falhas {preferenceId}</Card.Header>
                    <Card.Body>
                        <Form  onSubmit={saveOrUpdate}>
                            <Row className="mb-3">
                                <Form.Group as={Col} md="4" controlId="validationCustom01">
                                    <Form.Label>Nome</Form.Label>
                                    <Form.Control
                                        required
                                        type="text"
                                        name="name"
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        placeholder="Falhas de estouro de memória"                    
                                    />
                                    <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                                </Form.Group>

                                <Form.Group as={Col} md="5" controlId="formBasicSelect">
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
                                           <option key={i} value={pod.metric.pod}>{pod.metric.pod}/{pod.metric.namespace}</option>)                                        
                                            
                                        }
                                        
                       
                                    </Form.Control>
                                </Form.Group>

                                <Form.Group as={Col} md="3" controlId="formBasicSelect">
                                    <Form.Label>Metrica</Form.Label>
                                    <Form.Control
                                    as="select"
                                    name="metric"
                                    value={metric}
                                    onChange={e => {
                                        setMetric(e.target.value);
                                    }}
                                    >
                                        <option value="CPU">Cpu</option>
                                        <option value="DISCO">Disco</option>
                                        <option value="MEMORIA">Memória</option>
                                        <option value="REDE">Rede</option>
                                    </Form.Control>
                                </Form.Group>

                            </Row>                            
                            <Row className="mb-3">
                                <Form.Group as={Col} md="6" controlId="validationCustom02">
                                    <Form.Label>Tipo</Form.Label>
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
                                <Form.Group as={Col} md="3" controlId="validationCustom03">
                                    <Form.Label>Valor de Falha</Form.Label>
                                    <Form.Control 
                                        type="text" 
                                        placeholder="Ex. 1023975" 
                                        name="valueFailure"
                                        value={valueFailure}
                                        onChange={(e) => setValueFailure(e.target.value)}                                    
                                        required 
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        Por favor informe um valor de falha.
                                    </Form.Control.Feedback>
                                </Form.Group>
                                <Form.Group as={Col} md="3" controlId="validationCustom04">
                                    <Form.Label>Tempo em minuros</Form.Label>
                                    <Form.Control 
                                        type="text" 
                                        placeholder="Ex. 5M"
                                        name="periodTime"
                                        value={periodTime}
                                        onChange={(e) => setPeriodTime(e.target.value)} 
                                        required 
                                    />
                                    <Form.Control.Feedback type="invalid">
                                        Por favor invomer o valor médio
                                    </Form.Control.Feedback>
                                </Form.Group>

                            </Row>

                            <Row className="mb-3">
                                <Form.Group md={{ span: 3, offset: 9}} as={Col}>
                                    <Button variant="outline-secondary" style={{ marginRight:"5px" }}>cancelar</Button> 
                                    <Button variant="outline-primary" type="submit">Salvar</Button>                                                                           
                                </Form.Group>
                            </Row>
                        </Form>

                    </Card.Body>
                </Card>
            </div>

        </>
    )

}

export default FormPreferences;