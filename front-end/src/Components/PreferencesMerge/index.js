import React from "react";
import { useNavigate } from "react-router-dom"
import { Card, Row, Col } from "react-bootstrap"
import api from "../../Services/Api"
import CardTableMergeMetric from "../CardTablePreferences/CardTableMergeMetric";
import { AiOutlineDown, FiTrash } from "react-icons/ai";

const PreferencesMerge = () => {

    const [preferencesMerge, setPreferencesMerge] = React.useState([]);
    const [preferenceMergeCpu, setPreferencesMergeCpu] = React.useState([]);
    const [preferenceMergeDiskRd, setPreferencesMergeDiskRd] = React.useState([]);
    const [preferenceMergeDiskWd, setPreferencesMergeDiskWd] = React.useState([]);
    const [preferenceMergeMemory, setPreferencesMergeMemory] = React.useState([]);
    const [preferenceMergeNetworkRec, setPreferencesMergeNetworkRec] = React.useState([]);
    const [preferenceMergeNetworkSent, setPreferencesMergeNetworkSent] = React.useState([]);

    const [openCardCpu, setOpenCardCpu] = React.useState("none");
    const [openCardMemory, setOpenCardMemory] = React.useState("none");
    const [openCardDiskRc, setOpenCardDiskRc] = React.useState("none");
    const [openCardDiskWd, setOpenCardDiskWd] = React.useState("none");
    const [openCardRedeSend, setOpenCardRedeSend] = React.useState("none");
    const [openCardRedeTrans, setOpenCardRedeTrans] = React.useState("none");


    const handleCard = (opc, val) => {
        console.log(opc, val)
        switch (opc) {
            case 1:
                if (val === 'none')
                    setOpenCardCpu("block");
                else
                    setOpenCardCpu("none");
                break;
            case 2:
                if (val === 'none')
                    setOpenCardDiskRc("block");
                else
                    setOpenCardDiskRc("none");
                break;
            case 3:
                if (val === 'none')
                    setOpenCardDiskWd("block");
                else
                    setOpenCardDiskWd("none");
                break;
            case 4:
                if (val === 'none')
                    setOpenCardMemory("block");
                else
                    setOpenCardMemory("none");
                break;
            case 5:
                if (val === 'none')
                    setOpenCardRedeSend("block");
                else
                    setOpenCardRedeSend("none");
                break;
            case 6:
                if (val === 'none')
                    setOpenCardRedeTrans("block");
                else
                    setOpenCardRedeTrans("none");
                break;
        }

        //    if(openCard=== "none") {
        //        setOpenForm("block");
        //    }else
        //        setOpenForm("none");
    }

    const getPreferencesMerge = async () => {
        try {

            const resp = await api.get('/preferences/merge');
            const response = resp.data;
            setPreferencesMerge(response);
            const { CPU } = response
            const [cpu] = CPU
            const cpuValues = []
            const keys = Object.keys(cpu)
            keys.map(key => cpuValues.push({ pod: key, tempo: cpu[key][0], valor: cpu[key][1] }))
            setPreferencesMergeCpu(cpuValues)
            // Leitura de disco
            const { disk: { readNods } } = response;
            const [read] = readNods
            const diskRead = []
            keys.map(key => diskRead.push({ pod: key, tempo: read[key][0], valor: read[key][1] }))
            setPreferencesMergeDiskRd(diskRead)
            // Leitura de disco
            const { disk: { writeNods } } = response;
            const [write] = writeNods
            const diskWrite = []
            keys.map(key => diskWrite.push({ pod: key, tempo: write[key][0], valor: write[key][1] }))
            setPreferencesMergeDiskWd(diskWrite)
            // Memoria
            const { MEMORY } = response;
            const [memory] = response.MEMORY
            const memoryValues = []
            keys.map(key => memoryValues.push({ pod: key, tempo: memory[key][0], valor: memory[key][1] }))
            setPreferencesMergeMemory(memoryValues)

            // Network receive
            const { Network: { receive_bytes } } = response;
            const [receive] = receive_bytes
            const netReceive = []
            keys.map(key => netReceive.push({ pod: key, tempo: receive[key][0], valor: receive[key][1] }))
            setPreferencesMergeNetworkRec(netReceive)
            // Network receive
            const { Network: { transmit_bytes } } = response;
            const [transmit] = transmit_bytes
            const netTransmit = []
            keys.map(key => netTransmit.push({ pod: key, tempo: transmit[key][0], valor: transmit[key][1] }))
            setPreferencesMergeNetworkSent(netTransmit)


        } catch (error) {
            console.log(error);

        }
    }

    React.useEffect(() => {
        getPreferencesMerge();

    }, []);


    return (
        <>
            <div>
                <div >
                    <div style={{ padding: "10px", backgroundColor: "#007bff", color: "white", border: "solid" }}>
                        <Row>
                            <Col>
                                <h4>
                                    Consumo de Cpu dos Pods
                                </h4>
                            </Col>
                            <Col  md={{ span: 1, offset: 4}}>
                                <h4><AiOutlineDown onClick={() => { handleCard(1, openCardCpu) }}  /></h4>
                            
                            </Col>
                        </Row>
                    </div>
                    <div style={{ display: openCardCpu }}>
                        <CardTableMergeMetric
                            title="CPU"
                            mergeMetric={preferenceMergeCpu}
                        />
                    </div>
                </div>

                <div>
                    <div style={{ padding: "10px", backgroundColor: "#007bff", color: "white", border: "solid" }}>
                        <Row>
                            <Col>
                                <h4>
                                    Disco dos Pods Leitura

                                </h4>

                            </Col>
                            <Col md={{ span: 1, offset: 4}}>
                                <h4><AiOutlineDown onClick={() => { handleCard(1, openCardDiskRc) }} /></h4>
                            
                            </Col>
                        </Row>

                        
                    </div>
                    <div style={{ display: openCardDiskRc }}>
                        <CardTableMergeMetric
                            title="Leitura de Disco"
                            mergeMetric={preferenceMergeDiskRd}
                        />
                    </div>
                </div>

                <div>
                    <div style={{ padding: "10px", backgroundColor: "#007bff", color: "white", border: "solid" }}>
                        <Row>
                            <Col>
                                <h4>
                                    Disco dos Pods Escrita
                                </h4>
                            </Col>
                            <Col md={{ span: 1, offset: 4}}>
                                <h4><AiOutlineDown onClick={() => { handleCard(3, openCardDiskWd) }}/></h4>
                            </Col>
                        </Row>
                    </div>
                    <div style={{ display: openCardDiskWd }}>
                        <CardTableMergeMetric
                            title="Escrita de Disco"
                            mergeMetric={preferenceMergeDiskWd}
                        />
                    </div>
                </div>

                <div>
                    <div style={{ padding: "10px", backgroundColor: "#007bff", color: "white", border: "solid" }} >
                        <Row>
                            <Col>
                                <h4>
                                    Memoria dos Pods

                                </h4>
                            
                            </Col>
                            <Col md={{ span: 1, offset: 4}}>
                                <h4><AiOutlineDown onClick={() => { handleCard(4, openCardMemory) }} /></h4>
                            
                            </Col>
                        </Row>

                        
                    </div>
                    <div style={{ display: openCardMemory }}>
                        <CardTableMergeMetric
                            title="Memória"
                            mergeMetric={preferenceMergeMemory}
                        />
                    </div>

                </div>

                <div >
                    <div style={{ padding: "10px", backgroundColor: "#007bff", color: "white", border: "solid" }}>

                        <Row>
                            <Col>
                                <h4>
                                    Rede Bytes Recebidos

                                </h4>
                            
                            </Col>
                            <Col md={{ span: 1, offset: 4}}>
                                <h4><AiOutlineDown onClick={() => { handleCard(5, openCardRedeSend) }} /></h4>
                            
                            </Col>
                        </Row>

                        
                    </div>
                    <div style={{ display: openCardRedeSend }}>
                        <CardTableMergeMetric
                            title="Rede Bytes Recebidos"
                            mergeMetric={preferenceMergeNetworkRec}
                        />
                    </div>

                </div>

                <div >
                    <div style={{ padding: "10px", backgroundColor: "#007bff", color: "white", border: "solid" }}>
                        <Row>
                            <Col>
                                <h4>
                                    Rede Bytes Transmitido

                                </h4>
                            
                            </Col>
                            <Col md={{ span: 1, offset: 4}}>
                                <h4>
                                    <AiOutlineDown onClick={() => { handleCard(6, openCardRedeTrans) }}  />
                                </h4>
                            
                            </Col>
                        </Row>

                        
                    </div>
                    <div style={{ display: openCardRedeTrans }}>
                        <CardTableMergeMetric
                            title="Rede Bytes Enviados"
                            mergeMetric={preferenceMergeNetworkSent}
                        />
                    </div>

                </div>


            </div>

        </>
    )

}

export default PreferencesMerge;