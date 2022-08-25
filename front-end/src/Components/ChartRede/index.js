import React from "react";
import { Card } from "react-bootstrap"
import { Chart } from "react-google-charts";
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";

const ChartRede = () => {

    const [networkIO, setNetworkIO] = React.useState({})
    const [receive, setReceive] = React.useState([]);
    const [sent, setSent] = React.useState([]);


    const getNetworkIO = async () => {
        try {
            const testData = [["Tempo", "Receive", "Sent"]];
            const resp = await api.get('/network/io');
            const response = resp.data;
            const { receive, sent } = response;
            const { values: receiveValues } = receive[0]
            const { values: sentValues } = sent[0]
            receiveValues.forEach(receive => {
                const [time, receiveValue] = receive;
                const sentInTime = sentValues.find(sent => sent[0] === time);
                const sentValue = sentInTime && sentInTime.length ? sentInTime[1] : -1
                testData.push([Formats.formTimeStampToHours(time), Number(receiveValue), Number(sentValue)])
            })
            // console.log({ receiveValues, sentValues, times });
            setNetworkIO(response);
            setSent(testData)
        } catch (error) {
            console.error(error);
        }

    };

    React.useEffect(() => {
        getNetworkIO();

    }, []);

    // const dataSet = [["Hora", "KB"], [4, 5.5], [8, 12]];
    // console.log(dataSet);
    const data = [
        ["Year", "Sales", "Expenses"],
        ["2004", 1000, 400],
        ["2005", 1170, 460],
        ["2006", 660, 1120],
        ["2007", 1030, 540],
    ];

    const options = {
        width: "100%",
        height: "300px",
        intervals: { style:'line' },
        fontSize: "11",
        curveType: "function",
        legend: { position: "top" },
        series: [{ color: '#009578' }, {color: '#F79F1B' }],
        legendFontSize: "12",
        vAxes: {
            0: { title: "Kb/s" },
        },
        hAxes: {
            0: { title: "Horário" },
        },

    };

    return (
        <>
            <div>
                <Card className="text-center">
                    <Card.Header as="h4">Network I/O</Card.Header>
                    <Card.Body>
                        <Chart
                            chartType={"LineChart"}
                            data={sent}
                            options={options}
                            legendToggle
                        />
                    </Card.Body>
                </Card>
            </div>

        </>
    )

}

export default ChartRede;