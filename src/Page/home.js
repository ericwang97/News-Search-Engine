import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class Home extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="New's Data Integration System"/>
                <div className="row">
                    <Card title="Some notes" >
                    <div className="col-md-12">
                        <h5>Hey! Greeting from Liwei!</h5>
                        <h5>It's my first time making such an application, thank you for trying this!</h5>
                        <h5>This is a database search engine.</h5>
                        <h5>Backend: Python + Flask REST API + MySQL + Firebase</h5>
                        <h5>Front-end: REACT js + ANT design components</h5>
                        <div>&nbsp;&nbsp;</div>
                        <div>I do need a front-end designer to embellish my homepage lol (*╹▽╹*)</div>
                        <div>So hard to make a full stack application, thank you for the people who helped and supported me.</div>
                        <div>I did it!!!!!!!</div>
                        <div>&nbsp;&nbsp;</div>
                    </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="How to use" >
                        <div className="col-md-12">
                            <h5>Please use Search page to search whatever you want.</h5>
                            <div>The search results are based on the frequency of your sentence, as well as other features.</div>
                            <div>Note: I am trying to make it more like a real search engine as much as possible. Further analysis on NLP might be needed.</div>
                            <div>&nbsp;&nbsp;</div>
                            <h5>You can also click the table to take a look at the data</h5>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default Home;
