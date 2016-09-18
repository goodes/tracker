import React, { Component } from 'react';
import Package from './package';
import { Table, Td, Tr } from 'semantic-react';

export default class Packages extends Component {

	constructor(props) {
        super(props);
        this.packageCollection = this.props.packages;
        this.state = {
        	packages: [],
        	subscriber: null,
        };
	}

	componentDidMount() {
		// console.log('Packages: componentDidMount');
        var subscription = this.packageCollection.findAll({state: this.props.state }).order('tracking_id').watch().subscribe(
            (collection) => {
                if(collection) {
                    this.setState({packages: collection});
                }
            },
            (err) => {
                console.log(err);
            }
        );
        this.setState({subscriber: subscription});
	}

	// componentWillReceiveProps(nextProps) {
	// 	console.log('Packages: componentWillReceiveProps');
	// }

	componentWillUnmount() {
		// console.log('Packages: componentWillUnmount');
		if (this.state.subscriber) {
			this.state.subscriber.unsubscribe()
		}
	}

    render() {
    	const packagesMapped = this.state.packages.map((item, index) => {
    		return <Package key={index} package={item} packages={this.packageCollection} />
    	})
        return (
      		<div>
      		
        	<Table compact><thead>
        		<Tr>
	        		<th>Tracking ID</th>
	        		<th>Updated</th>
	        		<th>Image</th>
	        		<th>Status</th>
	        		<th>State</th>
	        		<th>Vendor</th>
	        		<th>&nbsp;</th>
        		</Tr>
        	</thead><tbody>
        	{packagesMapped}
        	</tbody></Table>
        	</div>
        );
    }
}
