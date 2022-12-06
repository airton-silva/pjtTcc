import React from "react";
import { Button, Card, CloseButton, Col, Dropdown, Form, InputGroup, Modal, Row, SplitButton, Table } from "react-bootstrap";
import { FiSearch } from "react-icons/fi"
import 'bootstrap/dist/css/bootstrap.min.css';

import FormPreferences from "../../Components/FormPreferencesMetrics";
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";



const SearchMetrics = () => {

    const [lgShow, setLgShow] = React.useState(false);


    const [typeQuery, setTypeQuery] = React.useState("query");
    const [myQuery, setMyQuery] = React.useState("");
    const [myDataSource, setMyDatasource] = React.useState("");
    const[filtro, setFiltro] = React.useState("");

    const [types, setTypes] = React.useState([]);
    const [typeMetric, setTypeMetric] = React.useState([]);
    const [valuesMetrics, setValuesMetrics]= React.useState([]);
    const [dataSources, setDataSources]= React.useState([]);
    const[listFilter, setListFilter]= React.useState([]);
   

    const showDataSources = async () => {

        try {
            const resp = await api.get('/data_sources');
            const response = resp.data
            setDataSources(response)
         
  

        } catch (error) {
            console.log(error);
            
        }

    }

    const allQuerys = async (e) => {
        e.preventDefault();

        const data = {            
            "url": myDataSource,
            "type":typeQuery,
            "query": myQuery    
        };
     
        try {

            const resp = await api.post('source', data)
            const response = resp.data.data.result; 
            setValuesMetrics(response)
            console.log(response)
            // setPods(response);
                        
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

	//buscar metrica por Namespace
	const getMetricsByNamespace = (filtro) => {
        console.log(filtro);
        console.log(valuesMetrics);
        const _metricas= valuesMetrics.map(val => (
        val.metric.namespace.toLowerCase().includes(filtro.toLowerCase())))

	};
   

    React.useEffect(() => {
        getTypesMetrics();
        showDataSources();
        // getPods();
  
    }, []);

    return (
        <>

            <div style={{ marginTop: '20px', boxShadow: '0 4px 8px 0 rgba(97, 94, 94, 0.2), 0 6px 20px 0 rgba(22, 21, 21, 0.19)', border: 'none' }}>
                <Card className="text-center">
                        <Card.Header as="h4">
                            Montar consulta
                        </Card.Header>
                        <Card.Body>
                            <Form onSubmit={allQuerys} >
                                <Row>
                                    
                                    <Form.Group as={Col} md="3" >                                     
                                        <Form.Label>Data Source</Form.Label>
                                        <Form.Control
                                        as="select"
                                        name="data_source"
                                        value={myDataSource}
                                        onChange={e => {
                                            setMyDatasource(e.target.value);
                                        }}
                                        >
                                            {
                                                dataSources.map((datasource, idx)=>{
                                                   const {id, name, url, } = datasource;
                                                   return (
                                                    <option key={id} value={url}>{name}</option>
                                                   )
                                                })   
                                            }

                                        </Form.Control>
                                                        
                                    </Form.Group>
              
                                    <Form.Group as={Col} md="9" >  
                                    <Form.Label>Busca</Form.Label>
                                        <InputGroup>
                                        
                                            <Form.Control
                                            placeholder="container_cpu_usage_total"
                                            name="myquery"
                                            value={myQuery}
                                            onChange={(e) => setMyQuery(e.target.value)}
                                            />
                                            <Button variant="outline-secondary" onClick={() => {setLgShow(true)}} ><FiSearch/></Button>
                                            <Button variant="outline-secondary" type="submit">Buscar</Button>
                                        </InputGroup>                                   
 
                                        
                                    </Form.Group>

                                </Row>


                            </Form>
  

                        </Card.Body>
                </Card>

                <Card className="text-center" >
                        <Card.Header as="h4"> 
                        <Row>

                            <span as={Col}>Metricas</span>
                            <Form inline>
                                                        
                                <InputGroup as={Col} md={{ span: 12, offset: 8 }}>
                                    <Form.Label>Filtro: </Form.Label>
                                
                                    <Form.Control
                                    placeholder="Namespaces"
                                    name="filtro"
                                    type="text"
                                    value={filtro}
                                    onChange={(e) => setFiltro(e.target.value)}
                                    />
                                    <Button variant="outline-secondary" onClick={() => {getMetricsByNamespace(filtro)}} ><FiSearch/></Button>                                    
                                    
                                    
                                </InputGroup>  
                            </Form>
                                 
                        </Row>
 
                                        
                                    
                        </Card.Header>
                            <Card.Body>
                                <Table responsive hover size="sm">
                                        
                                        <thead>
                                            <tr>                   
                                                <th>Metrica</th>
                                                <th>Container</th> 
                                                <th>Namespace</th>
                                                <th>Job</th>
                                                <th>Instancia</th>
                                                <th>Pod</th>
                                                <th>tempo</th>
                                                <th>Valor</th>
                                                         
                                    
                                            </tr>
                                        </thead>
                                        <tbody>
                                        { listFilter.length === 0 ?
                                            valuesMetrics.map((val, idx)=>{
                                                const { metric, value } = val;
                                                
                                                return (
                                                    <tr key={idx}>
                                                        <td>{metric.__name__}</td>
                                                        <td>{metric.container}</td>
                                                        <td>{metric.namespace}</td>
                                                        <td>{metric.job}</td>
                                                        <td>{metric.instance}</td>
                                                        <td>{metric.pod}</td>
                                                        <td>{Formats.formTimeStampToHours(value[0])}</td>
                                                        <td>{value[1]}</td>
                                                    </tr>
                                                );
                                                
                                            }) :
                                            
                                            listFilter.map((val, idx)=>{
                                                const { metric, value } = val;
                                                
                                                return (
                                                    <tr key={idx}>
                                                        <td>{metric.__name__}</td>
                                                        <td>{metric.container}</td>
                                                        <td>{metric.namespace}</td>
                                                        <td>{metric.job}</td>
                                                        <td>{metric.instance}</td>
                                                        <td>{metric.pod}</td>
                                                        <td>{Formats.formTimeStampToHours(value[0])}</td>
                                                        <td>{value[1]}</td>
                                                    </tr>
                                                );
                                                
                                            })
                                        }                                            
                                            
                                        </tbody>
                                </Table>
                            </Card.Body>
                </Card>
   
            </div>

            <Modal
            size="lg"
            show={lgShow}
            onHide={() => setLgShow(false)}
            aria-labelledby="example-modal-sizes-title-lg"
            >
            <Modal.Header>
                
            <Modal.Title id="example-modal-sizes-title-lg">
            Tipo de Metricas <CloseButton className="close" onClick={()=>setLgShow(false)}/>
            </Modal.Title>
            </Modal.Header>
            <Modal.Body>

                <Form.Control
                    as="select"
                    name="type"
                    // value={type}
                    onChange={e => {
                    setMyQuery(e.target.value);
                    }}
                    >
                        
                        { 
                        typeMetric.map((type,i)=>
                        <option key={i} value={type}>{type}</option>)                                        
                            
                        }
                        

                    </Form.Control>
            </Modal.Body>
            </Modal>

        </>
    )

}

export default SearchMetrics;