import React from "react";
import { Card, Table} from "react-bootstrap"
import Formats from "../../Utils/Formats";

const CardTableMergeMetric = (prop) => {

    const {title, mergeMetric}= prop;


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
                            
                                    </tr>
                                </thead>
                                <tbody>
                                {
                                    mergeMetric.map((preference, idx)=>{
                                        const { pod, tempo, valor } = preference;
                                        
                                        return (
                                            <tr key={idx}>
                                                <td>{pod}</td>
                                                <td>{tempo}</td>
                                                <td>{valor}</td>
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