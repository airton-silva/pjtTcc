import React from "react";
import ClusterServices from "../../Components/ClusterServices";
import MetricsHost from "../../Components/MetricsHost";
import ChartRede from "../../Components/ChartRede";


const Home = () => {   
    return (
        <>   

            <div style={{ marginTop:'20px', boxShadow:'0 4px 8px 0 rgba(97, 94, 94, 0.2), 0 6px 20px 0 rgba(22, 21, 21, 0.19)', border:'none'}}>
                <ChartRede />
                <MetricsHost />
                <ClusterServices />                
            </div>        
            
        </>
    )

}

export default Home;
