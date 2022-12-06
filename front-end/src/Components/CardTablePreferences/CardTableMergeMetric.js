import React from "react";
import { Card, Table} from "react-bootstrap"
import Formats from "../../Utils/Formats";
import {FiAlertCircle} from "react-icons/fi"
import api from "../../Services/Api"

const CardTableMergeMetric = (prop) => {

    const {title, mergeMetric}= prop;
    console.log("*", ...mergeMetric)

    const [alert, setAlert] = React.useState()

    const getAlert = async (pod) => {
        console.log(pod)
        try {
            const resp = await api.get(`/alerts/${pod}`);
            const response = resp.data;
            setAlert(response);
            console.log("alert=",response)

                        
        } catch (error) {
            console.log(error);
            
        }
    }


    return (
        <>
            <Card className="text-center" >
                <Card.Header as="h4">Metricas de {title}</Card.Header>
                    <Card.Body>
                        <Table responsive hover size="sm">
                                
                                <thead>
                                    <tr>                   
                                        <th>Container</th>
                                        <th>Tempo</th> 
                                        <th>Valor</th> 
                                        {/* <th>alerts</th>              */}
                            
                                    </tr>
                                </thead>
                                <tbody>
                                {
                                    mergeMetric.map((preference, idx)=>{
                                        const { pod, tempo, valor } = preference;
                                        
                                        return (
                                            <tr key={idx}>
                                                <td>{pod}</td>
                                                <td>{Formats.formatTimesStampToDateTime(tempo)}</td>
                                                <td>{valor}</td>
                                                {/* {valor > 0.0300000000
                                                &&(<td><FiAlertCircle color="red"  onClick={getAlert(pod)}/></td>)} */}
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

export default CardTableMergeMetric;