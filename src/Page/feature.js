import React from 'react';
import PageTitle from '../Component/page-title.js';
import './home.css'
import { Card } from "antd";
import 'antd/es/card/style/css'; // 加载 CSS

class Feature extends React.Component{


    render(){
        return(
            <div id="page-wrapper">
                <PageTitle title="Feature Description"/>
                <div className="row">
                    <Card title="1. Search Engine" >
                        <div className="col-md-12">
                            <h5>Search Engine is based on...</h5>
                            <div>Phrase frequency, etc. </div>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="2. New's crawler" >
                        <div className="col-md-12">
                            <h5>New's crawler is based on...</h5>
                            <div>Daily crawler</div>
                            <div>后端爬到数据，做个search engine放前端展示，前端如果需要更多额外的topic的话，返回后端继续爬新的数据，越来越增大数据库</div>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="3. NLP Processing and Analysis, and Recommendation" >
                        <div className="col-md-12">
                            <h5>NLP Processing and Analysis is based on...</h5>
                            <div>后期加上点赞，除了search engine再加点NLP的内容，比如可以做根据点赞的文本算文本相似度之类做个非常简单的推荐。</div>
                            <div>加入近义词自动识别</div>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>
                    <div>&nbsp;&nbsp;</div>
                    <div>&nbsp;&nbsp;</div>
                    <Card title="4. Database Presentation" >
                        <div className="col-md-12">
                            <h5>Database Presentation is based on...</h5>
                            <div>Used World, Film, Customers Orders database as the examples to show the presentation of database, including their FK relationships. </div>
                            <div>&nbsp;&nbsp;</div>
                        </div>
                    </Card>

                </div>
            </div>


        );
    }
}

export default Feature;
