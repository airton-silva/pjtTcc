import React from "react";
import {useNavigate} from "react-router-dom"
import { Card,Table, Modal, CloseButton } from "react-bootstrap"
import api from "../../Services/Api"
import FormPreferences from "../FormPreferencesMetrics";
import { FiEdit, FiTrash } from "react-icons/fi";

import "./style.css";

const ShowPreferences = () => {

    const [preferences, setPreferences] = React.useState([]);
    const [preferenceId, setPreferenceId] = React.useState("");
    const [lgShow, setLgShow] = React.useState(false);
    let navigate = useNavigate();
    const getPreferences = async () => {
        try {

            const resp = await api.get('/preferences');
            const response = resp.data; 
            setPreferences(response);
                        
        } catch (error) {
            console.log(error);
            
        }
    }

    const deletePreferences = async (id) => {
        
        try {
            
            const resp = await api.delete(`/preferences/${id}`);
            console.log(id);


                                      
        } catch (error) {
            console.log(error);
            
        }
    }

    React.useEffect(() => {
        getPreferences();

    }, []);

    return (
        <>
            <div>
                <Card className="text-center">
                    <Card.Header as="h4">Suas definições de falha</Card.Header>
                    <Card.Body>
                        <Table responsive hover size="sm">
                            
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Nome</th> 
                                    <th>Serviços</th> 
                                    <th>Metrica</th> 
                                    <th>Tipo</th> 
                                    <th>Vlr. de Falha</th>
                                    <th>Intervalo Tempo</th>
                                    <th>Opções</th>
                        
                                </tr>
                            </thead>
                            <tbody>
                                    
                                {preferences.map((preference, index) => (
                                    <tr key={index}>
                                        <td>{preference.id}</td>
                                        <td>{preference.name}</td>
                                        <td>{preference.name_pod}</td>
                                        <td>{preference.metric}</td>
                                        <td>{preference.type}</td>
                                        <td>{preference.value_failure}</td>
                                        <td>{preference.period_time}</td>
                                        <td>
                                            <FiEdit color="orange" title="editar" 
                                                style={{ marginRight:"10px", cursor:"pointer" }} 
                                                onClick={() => {setLgShow(true); setPreferenceId(preference.id)}}                                                
                                                values={preferenceId}
                                                
                                            />
                                            <FiTrash color="red" title="apagar" 
                                                style={{ cursor:"pointer" }} 
                                                onClick={(e) => {window.confirm("deseja realmentte realizar esta ação") && deletePreferences(preference.id)}}/>
                                        </td>
                                    
                                    </tr>
                                ))}                        
                                
                                
                            </tbody>
                        </Table>
                    </Card.Body>
                </Card>

                <Modal
                    size="lg"
                    show={lgShow}
                    onHide={() => setLgShow(false)}
                    aria-labelledby="example-modal-sizes-title-lg"
                >
                    <Modal.Header>
                        
                    <Modal.Title id="example-modal-sizes-title-lg">
                        Large Modal <CloseButton className="close" onClick={()=>setLgShow(false)}/>
                    </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <FormPreferences show={null} preferenceId={preferenceId} />
                    </Modal.Body>
                </Modal>

            </div>

        </>
    )

}

export default ShowPreferences;