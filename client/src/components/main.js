import React, { Component } from 'react';

import Horizon from '../horizon-container';
import Packages from './packages';
import { Link, IndexLink } from 'react-router';

const _horizon = Horizon.get();
const _packageCollection = _horizon('items');

export default class MessageContainer extends Component {

    constructor(props) {
	    super(props);
	    this.state = {
	    	text: '', 
	    	errorDescription: '',
	    };
	}

	// componentWillMount() {
	// 	console.log('Main:  componentWillMount');
	// }

	// componentWillReceiveProps(nextProps) {
	// 	console.log('Main: componentWillReceiveProps');
	// }

	// componentWillUnmount() {
	// 	console.log('Main: componentWillUnmount');
	// }


    render() {
        return (
	        <div>
	        	<Link to="/new"><button>New</button></Link>
	        	<p/>
	        	<Packages packages={_packageCollection} state="open"/>
	        	<p/>
	        	<Packages packages={_packageCollection} state="delivered"/>
            </div>
        );
    }
}