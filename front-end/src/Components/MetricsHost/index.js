import React from "react";
import { Card, Row, Col } from "react-bootstrap";
import api from "../../Services/Api"
import Formats from "../../Utils/Formats";
import "./style.css";

const MetricsHost = () => {

    const [MemoryTotalHost, setMemoryTotalHost] = React.useState("");
    const [consumoMemory, setConsumoMemory] = React.useState("");
    const [percentMemoryUsage, setPercentmemoryUsage] = React.useState("");

    const [CpuTotalHost, setCpuTotalHost] = React.useState("");
    const [consumoCpu, setConsumoCpu] = React.useState("");
    const [percentCpuUsage, setPercentCpuUsage] = React.useState("");

    const [DiskTotalHost, setDiskTotalHost] = React.useState("");
    const [consumoDisk, setConsumoDisk] = React.useState("");
    const [percentDiskUsage, setPercentDiskUsage] = React.useState("");
   


    const getMemoryHost = async () => {
        try {
            const { data: { data: { result } } } = await api.get('/memory');
            const response = Formats.formatBytes(result[0].value[1]);
            setMemoryTotalHost(response);
        } catch (error) {
            console.error(error);
        }

    };

    const getPercentMemoryConsume = async () => {
        try {
            const { data: { data: { result } } }= await api.get('/percent-memory');
            const response = result[0].value[1];
            setPercentmemoryUsage(response);
            
        } catch (error) {
            console.error(error);
        }

    };

    const getMemoryConsume = async () => {
        try {
            const { data: { data: { result } } }= await api.get('/memory-usage');
            const response = Formats.formatBytes(result[0].value[1]);
            setConsumoMemory(response);
            
        } catch (error) {
            console.error(error);
        }

    };

    const getCpuHost = async () => {
        try {
            const { data: { data: { result } } } = await api.get('/cpu');
            const response = result[0].value[1];
            setCpuTotalHost(response);
        } catch (error) {
            console.error(error);
        }

    };

    const getCpuConsume = async () => {
        try {
            const { data: { data: { result } } }= await api.get('/cpu-usage');
            const response = Number(result[0].value[1]).toFixed(2);
            setConsumoCpu(response);
            
        } catch (error) {
            console.error(error);
        }

    };

    const getPercentCpuConsume = async () => {
        try {
            const { data: { data: { result } } }= await api.get('/percent-cpu');
            const response = result[0].value[1];
            setPercentCpuUsage(response);
            
        } catch (error) {
            console.error(error);
        }

    };

    const getDiskHost = async () => {
        try {
            const { data: { data: { result } } } = await api.get('/filesystem');
            const response = Formats.formatBytes(result[0].value[1]);
            setDiskTotalHost(response);
        } catch (error) {
            console.error(error);
        }

    };

    const getPercentDiskConsume = async () => {
        try {
            const { data: { data: { result } } }= await api.get('/filesystem_percent');
            const response = result[0].value[1];
            setPercentDiskUsage(response);
            
        } catch (error) {
            console.error(error);
        }

    };

    const getDiskConsume = async () => {
        try {
            const { data: { data: { result } } }= await api.get('/filesystem_usage');
            const response = Formats.formatBytes(result[0].value[1]);
            setConsumoDisk(response);
            
        } catch (error) {
            console.error(error);
        }

    };

    React.useEffect(() => {
        getMemoryHost();
        getPercentMemoryConsume();
        getMemoryConsume();
        getCpuHost();
        getCpuConsume();
        getPercentCpuConsume();
        getDiskHost();
        getDiskConsume();
        getPercentDiskConsume();
    }, []);

    const styleMemory = Formats.styleGauge(percentMemoryUsage);
    const styleCpu = Formats.styleGauge(percentCpuUsage);
    const styleDisk = Formats.styleGauge(percentDiskUsage);
 

    return (
        <>
            <div>
                <Card className="text-center">
                    <Card.Header as="h4"> Metricas de Host </Card.Header>
                    <Card.Body className="vlh">
                        <Row>
                            <Col>
                                <Col md={12}>
                                    <h4>Memória</h4>
                                    <div className="gauge">
                                        <div className="gauge__body">
                                            <div className="gauge__fill" style={styleMemory} ></div>
                                            <div className="gauge__cover"> {Number(percentMemoryUsage).toFixed(2)}%</div>
                                        </div>
                                    </div>
                                    {/* <div className="circle gradient"></div> */}
                                </Col>
                                <Row>
                                    <Col md={5} className="vlm-1">
                                        <h4>Usada</h4>
                                        {consumoMemory}
                                    </Col>
                                    <Col md={5} className="vlm-2">
                                        <h4>Total</h4>
                                        {MemoryTotalHost}
                                    </Col>

                                </Row>

                            </Col>
                            <Col>
                                <Col md={12}>
                                <h4>Cpu</h4>
                                    <div className="gauge">
                                        <div className="gauge__body">
                                            <div className="gauge__fill" style={styleCpu} ></div>
                                            <div className="gauge__cover"> {Number(percentCpuUsage).toFixed(2)}%</div>
                                        </div>
                                    </div>
                                    {/* <div className="circle gradient"></div> */}
                                </Col>
                                <Row>
                                    <Col md={5} className="vlm-1">
                                        <h4>Usada</h4>
                                        {consumoCpu}
                                    </Col>
                                    <Col md={5} className="vlm-2">
                                        <h4>Total</h4>
                                        {CpuTotalHost}
                                    </Col>

                                </Row>

                            </Col>
                            <Col>
                                <Col md={12}>
                                <h4>Disco</h4>
                                    <div className="gauge">
                                        <div className="gauge__body">
                                            <div className="gauge__fill" style={styleDisk} ></div>
                                            <div className="gauge__cover"> {Number(percentDiskUsage).toFixed(2)}%</div>
                                        </div>
                                    </div>
                                    {/* <div className="circle gradient"></div> */}
                                </Col>
                                <Row>
                                    <Col md={5} className="vlm-1">
                                        <h4>Usada</h4>
                                        {consumoDisk}
                                    </Col>
                                    <Col md={5} className="vlm-2">
                                        <h4>Total</h4>
                                        {DiskTotalHost}
                                    </Col>

                                </Row>

                            </Col>
                        </Row>
                    </Card.Body>



                </Card>

            </div>
        </>
    )

}

export default MetricsHost;