import React, { Component } from 'react';
import './CustomNav.css';

export default class CustomNav extends Component {
    render() {
        return (
            <nav className="navbar navbar-expand-lg bg-white">
                <a className="navbar-brand" href="#"><i className="fa fa-2x fa-product-hunt"></i></a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item active">
                            <a className="nav-link" href="#">Ask <span className="sr-only">(current)</span></a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="#">Ship</a>
                        </li>
                        <li className="nav-item">
                            <a className="nav-link" href="#">Jobs</a>
                        </li>
                    </ul>
                    <ul className="navbar-nav ml-auto">
                        <li  className="nav-item active">
                            <button id="login-btn" className="btn btn-primary" href="#">Log In <span className="sr-only">(current)</span></button>
                        </li>
                    </ul>
                </div>
            </nav>
        )
    }
}