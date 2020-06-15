import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class Crawler extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="Run Crawler"/>
                <div className="row">
                    <Card title="Some notes" >
                        <div className="col-md-12">
                            <h5>Run the Crawler to get your own topic of news</h5>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default Crawler;
