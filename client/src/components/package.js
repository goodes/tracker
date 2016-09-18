import React, { Component } from 'react';
import { Button, Tr, Td, Icon } from 'semantic-react';
import { Flag } from 'semantic-react';
import { Link, IndexLink } from 'react-router';

export default class Package extends Component {


	constructor(props) {
        super(props);
        this.packageCollection = this.props.packages;
        this.item = this.props.item;
        this.handleClick = this.handleClick.bind(this);

	}


	handleClick(e) {
		this.packageCollection.update({
		 	id: this.props.package.id,
		 	state: this.props.package.state === "open" ? 'delivered' : 'open'
		});
	}

    render() {
        let item = this.props.package;
        let state = item.state === "open" ? "Close" : "Open";
		let emphasis = item.state === "open" ? "positive" : "negative";
        return ( <Tr>
			<Td><Link to={`/edit/${item.id}`}>{item.tracking_id}</Link></Td>
			<Td><a href={item.link} target="_blank"><Icon name="external"/></a> {item.ts.toDateString()}</Td>
            <Td><img src={item.image_url} heigh={30} width={30}/></Td>
			<Td>{item.status}</Td>
			<Td>{item.state}</Td>
            <Td>{item.vendor}</Td>
			<Td><Button emphasis={emphasis} size="mini" onClick={this.handleClick}>{state}</Button></Td>
			</Tr>
        );
    }
}

// <Flag name="Israel"/>
