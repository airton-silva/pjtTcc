import React from "react";
import { Card } from "react-bootstrap"
import { Chart } from "react-google-charts";
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";
import MetricsHost from "../MetricsHost";
import _ from "lodash";


const CpuContainerMetrics = () => {

    const [consumeCpuContainer, setConsumeCpuContainer] = React.useState({});
    const [dataSet, setDataSet] = React.useState([]);

    const getCpuConsume = async () => {
        try {
            const data = [["cores", "container"]];
            const resp = await api.get('/cpu/container');
            const response = resp.data;
            const { cpu_consume } = response;

            // const ts = _.groupBy(cpu_consume.metric.image)
            
            
            const nameContainer = cpu_consume.map((val, key)=> {
                const cores = Number(val.value[1])
                const time = Formats.formTimeStampToHours(val.value[1])
            
                return [val.metric.image+'/'+val.metric.name, cores]
            });
            
            data.push(...nameContainer)
  
            setDataSet(data)
            
            // const mag= [nameP,...ts]
            setDataSet(data)
            // console.log(mag)
            // const data = [["Tempo", "Nome", "Consumo"]];
            // const resp = await api.get('/graf/consume_cpu_by_container');
            // const response = resp.data.data.result;
            // const times = response[0].values.map(value => value[0]);
            // const seiLa = []
            // const objects = response.forEach(({ metric: { image, name }, values }) => {
            //     const _name = `${image}-${name}`;
            //     values.forEach(value => seiLa.push({ name: _name, time: value[0], consume: value[1]  }))
            //     // data.push(_values)
            //     // return ({ name: _name, values: _values });
            // });
            // const teste = times.map(time => {
            //     const interest = seiLa.filter(({ time: timeA }) => timeA === time);
            //     data.push([Formats.formTimeStampToHours(time), [0,1,2,3,4,5], [321,432,45345,323,456,47657]])
            //     // interest.forEach(({ name, time, consume }, index) => data.push([Formats.formTimeStampToHours(time), [0,1,2,3,4,5], Number(consume)]))
            // });
            // console.log(response)
            // console.log({ times });
            // console.log({ names });
            // console.log({ data });
            // const arr =[[ 1669291301.27, 0.008306185264153628 ],[ 1669291301.27, 0.008306185264153628 ],[ 1669291301.27, 0.008306185264153628 ]]
            // const nameP =[]
            // const ts = response.map((res, idx)=>{
            //     nameP.push(res.metric.image)
            //     return [res.values[idx]]
            // })
            
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
        intervals: { style: 'line' },
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