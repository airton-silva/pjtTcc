import React from "react";
import { Card } from "react-bootstrap"
import { Chart } from "react-google-charts";
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";

const CpuContainerMetrics = () => {

    const [consumeCpuContainer, setConsumeCpuContainer] = React.useState({});
    const [dataSet, setDataSet] = React.useState([]);

    const getCpuConsume = async () => {
        try {
            const data = [["cores", "container"]];
            const resp = await api.get('/cpu/container');
            const response = resp.data;
            const { cpu_consume } = response;
           
            const nameContainer = cpu_consume.map((val, key)=> {
                const cores = Number(val.value[1])
                const time = Formats.formTimeStampToHours(val.value[1])
                // return [time, cores]
                return [ val.metric.image+'/'+val.metric.name, cores]
            });
             

            data.push(...nameContainer)
            
            // console.log("nameContainersp", response);
            // console.log(nameContainer)
            setDataSet(data)

            
        } catch (error) {
            console.log(error);
            
        }
    }

    React.useEffect(() => {
        getCpuConsume();

    }, []);

    const options = {
        width: "100%",
        height: "300px",
        intervals: { style:'line' },
        fontSize: "11",
        curveType: "function",
        legend: { position: "top" },
        legendFontSize: "12",
        vAxes: {
            0: { title: "Cores" },
        },
        hAxes: {
            0: { title: "Containers" },
        },

    };

    return (
        <>
            <div>
                <Card className="text-center">
                    <Card.Header as="h4">Consumo de Cpu/Container</Card.Header>
                    <Card.Body>
                        <Chart
                            chartType={"LineChart"}
                            data={dataSet}
                            options={options}
                            legendToggle
                        />
                    </Card.Body>
                </Card>
            </div>

        </>
    )

}

export default CpuContainerMetrics;