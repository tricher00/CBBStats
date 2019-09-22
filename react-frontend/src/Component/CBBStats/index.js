import React, { Component } from "react";

import axios from "axios";

function getName(school, index){
    return (<h2>{index}</h2>)
}

export default class School extends Component {
  constructor(props) {
    super(props);
    this.state = {
    school:[],
    };
    this.loadSchools = this.loadSchools.bind(this);
  }

  componentWillMount() {
    this.loadSchools();
  }

  async loadSchools()
  {
    const promise = await axios.get("http://localhost:8000/api/schools/26/");
    const status = promise.status;
    if(status===200)
    {
      const data = promise.data.data;
      this.setState({school:data});
    }
  }

  render() {
    return(
      <div>
        <h1>Schools</h1>
        <h2>{this.state.school.name}</h2>
      </div>
    )
  }
}

