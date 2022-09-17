import React from "react";
import { Button, Card, Col, Form, Row, Table,} from "react-bootstrap";
import { FiEdit, FiTrash } from "react-icons/fi";
import api from "../../Services/Api"


const DataSources = () => {

    const [dataSources, setDataSources] = React.useState([]);
    const [name, setName] = React.useState("");
    const [url, setUrl] = React.useState("");
    const [authType, setAuthType] = React.useState("");

    const [openForm, setOpenForm] = React.useState("none");

    const createDataSources = async (event) => {
        event.preventDefault();

        const data = {
            "name":name,
            "url": url,
            "authType": authType    
        };

        try {
            const resp = await api.post('/data_sources', data);
            alert("Data Source  "+ resp.data.name+ "\n Criado com sucesso");
            clearForm();
            setOpenForm("none");
            showDataSources();

        } catch (error) {
            console.log(error);
            
        }

    }

    const clearForm = ()=>{
        setAuthType("");
        setName("");
        setUrl("");
    }

    const showDataSources = async () => {

        try {
            const resp = await api.get('/data_sources');
            const response = resp.data
            setDataSources(response)
  

        } catch (error) {
            console.log(error);
            
        }

    }


    const deleteDataSource = async (id) => {
        
        try {
            
            const resp = await api.delete(`/data_sources/${id}`);
            console.log(id);
            showDataSources();


                                      
        } catch (error) {
            console.log(error);
            
        }
    }


    const handleForm = () => {
 
       if(openForm === "none") {
           setOpenForm("block");
       }else
           setOpenForm("none");
    }

    React.useEffect(() => {
        showDataSources();

    }, []);

    return (
        <>
                <Card className="text-center">
                    <Card.Header as="h4">
                        Data Sources de Monitoramento
                        <Button  as={Col} md={{ span: 1, offset: 5}} onClick={handleForm}>add</Button>
                    </Card.Header>
                    <Card.Body>
                        {/* cardForm */}
                        <Card className="text-center" style={{ display: openForm }}>
                            <Card.Header as="h4">Add Data Sources de Monitoramento</Card.Header>
                            <Card.Body>
                                <Form  onSubmit={createDataSources}>
                                    <Row className="mb-3">
                                        <Form.Group as={Col} md="4" controlId="validationCustom01">
                                            <Form.Label>Nome</Form.Label>
                                            <Form.Control
                                                required
                                                type="text"
                                                name="name"
                                                value={name}
                                                onChange={(e) => setName(e.target.value)}
                                                placeholder="nome"                    
                                            />
                                            <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                                        </Form.Group>
                                        <Form.Group as={Col} md="4" controlId="validationCustom02">
                                            <Form.Label>host</Form.Label>
                                            <Form.Control
                                                required
                                                type="text"
                                                name="url"
                                                value={url}
                                                onChange={(e) => setUrl(e.target.value)}
                                                placeholder="localhost:9000/api/"                    
                                            />
                                            <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                                        </Form.Group>
                                        <Form.Group as={Col} md="4" controlId="validationCustom03">
                                            <Form.Label>Auth</Form.Label>
                                            <Form.Control
                                                required
                                                type="text"
                                                name="authType"
                                                value={authType}
                                                onChange={(e) => setAuthType(e.target.value)}
                                                placeholder="Beare"                    
                                            />
                                            <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                                        </Form.Group>


                                    </Row>

                                    <Row className="mb-3">
                                        <Form.Group md={{ span: 3, offset: 9}} as={Col}>
                                            <Button variant="outline-secondary" style={{ marginRight:"5px" }} onClick={handleForm}>cancelar</Button> 
                                            <Button variant="outline-primary" type="submit">Salvar</Button>                                                                        
                                        </Form.Group>
                                    </Row>
                                </Form>

                            </Card.Body>
                        </Card>
                        <Table responsive hover size="sm">
                                
                                <thead>
                                    <tr>                   
                                        <th>Data Source</th>
                                        <th>url Base</th> 
                                        <th>Autenticação tipo</th>
                                        <th>Opções</th>             
                            
                                    </tr>
                                </thead>
                                <tbody>
                                {
                                    dataSources.map((datasource, idx)=>{
                                        const {id, name, url, authType } = datasource;
                                        
                                        return (
                                            <tr key={idx}>
                                                <td>{name}</td>
                                                <td>{url}</td>
                                                <td>{authType}</td>
                                                <td>
                                                    <FiTrash color="red" title="apagar" 
                                                    style={{ cursor:"pointer" }} 
                                                    onClick={(e) => {window.confirm("deseja realmentte realizar esta ação") && deleteDataSource(id)}}/>
                                                </td>
                                            </tr>
                                        );
                                        
                                    })
                                }                                            
                                    
                                </tbody>
                        </Table> 

                    </Card.Body>
                </Card>
        </>

    
    )

}

export default DataSources;