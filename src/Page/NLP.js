import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class NLP extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="NLP Analysis"/>
                <div className="row">
                    <Card title="Some notes" >
                        <div className="col-md-12">
                            <h5>Trying to do something about NLP!</h5>
                            <div>Try to favorite something, and I will update the database and send more accurate news results for you.</div>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default NLP;
