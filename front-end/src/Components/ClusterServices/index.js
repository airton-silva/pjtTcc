import React from "react";
import { Card, Table } from "react-bootstrap";
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";
// import "./style.css"

const ClusterServices = () => {

    const [targetsUp, setTargetsUp] = React.useState([]);

    const getTargtsUp = async () => {
        try {
            const {data:{data:{activeTargets}}} = await api.get('/');
            const response = activeTargets;
            setTargetsUp(response);
        } catch (error) {
            console.error(error);	
        }

    };

    React.useEffect(() => {
        getTargtsUp();
	}, []);

 
    return (
        <>
            <div>
                <Card className="text-center">
                    <Card.Header as ="h4"> Serviços Rodando no Cluster </Card.Header>
                    <Table responsive>
                        
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Serviços</th> 
                                <th>Instancia</th> 
                                <th>Status</th> 
                                <th>Ult. Scrape</th>
                    
                            </tr>
                        </thead>
                        <tbody>
                                
                            {targetsUp.map((targets, index) => (
                                <tr key={index}>
                                    <td>{index+1}</td>
                                    <td>{targets.labels.job}</td>
                                    <td>{targets.labels.instance}</td>
                                    <td>{targets.health}</td>
                                    <td>{Formats.formatTimesStampToDateTime(targets.lastScrape)}</td>
                                
                                </tr>
                            ))}                        
                            
                            
                        </tbody>
                    </Table>
                    
                </Card>

            </div>
        </>
    )

}

export default ClusterServices;