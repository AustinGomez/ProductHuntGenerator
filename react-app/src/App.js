import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import CustomNav from './Components/CustomNav';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      products: []
    };
  }

  componentDidMount() {
    fetch("http://localhost:5000/api/products")
      .then(res => res.json())
      .then(
      (result) => {
        this.setState({
          isLoaded: true,
          products: result.products
        }, console.log(this.state));
      },
      // Note: it's important to handle errors here
      // instead of a catch() block so that we don't swallow
      // exceptions from actual bugs in components.
      (error) => {
        this.setState({
          isLoaded: true,
          error
        });
      }
      )
  }
  render() {
    return (
      <div className="App">
        <CustomNav />
        <div className="jumbotron lead-jumbo justify-content-center">
          <div className="container"> 
            <h1 className="d-4">ProductHunt, but it's all generated by a neural network.</h1>
            <p className="lead">I fed some data through this. Here's some ideas.</p>
          </div>
        </div>
        <div className="container">
          <div className="row">
            <div className="col-3">
              <div className="col col-sm-0 d-flex category-row flex-column text-left feed-box">
                <div className="feed-row mb-0 row">
                  <div className="col mr-auto feeds-text mb-2">
                    Feeds
                  </div>
                </div>
                <span className="mb-1">Yours</span>
                <span className="mb-1">Home</span>
                <span className="mb-1">Tech</span>
                <span className="mb-1">Productivity</span>
              </div>
            </div>
            <div className="col-sm-12 col-md-7">
              {
                this.state.products ? this.state.products.map((product, index) => {
                  return (
                    <div className="row product-box" key={index}>
                      <div className="col-md-2 col-4">
                        <img className="product-icon" src={require('./images/producthunt.png')} />
                      </div>
                      <div className="col text-left">
                        <h4>
                          {product.name}
                        </h4>
                        <div className="mr-auto text-muted">
                          {product.tagline}
                        </div>
                        <div className="badge badge-danger mr-auto">
                          Productivity
                      </div>
                      </div>
                    </div>
                  )
                }) : "loading"
              }
            </div>
            <div className="col-md-2">
            </div>
          </div>
        </div>
      </div >
    );
  }
}

export default App;
