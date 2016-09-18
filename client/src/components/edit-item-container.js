import React, { Component } from 'react';
import Horizon from '../horizon-container';
import { Form, Field, Header, Fields, Container, Input, Icon, Checkbox, Button } from 'semantic-react';
import ReactDOM from 'react-dom';
import { Link } from "react-router";

const _horizon = Horizon.get();
_horizon.connect();
const _packageCollection = _horizon('items');


class EditItem extends Component {
	constructor(props) {
        super(props);
        this.handleEdit = this.handleEdit.bind(this)
        this.updateRecord = this.updateRecord.bind(this)
        this.state = {
        	item: {
				tracking_id: '',
				vendor: '',
				title: '',
				link: '',
				status: '',
				ts: new Date(),
				state: 'open',
			},
        	loading: true
        };
	}

	updateFromBackend() {
        _packageCollection.find(this.props.routeParams.id).fetch().subscribe(
            (item) => {
                if(item) {

                    this.setState({
                    	item: item, 
                    	loading: false,
			        });
                }
            },
            (err) => {
                console.log(err);
            }
        );

		}

	componentDidMount(nextProps) {
		this.props.routeParams.id 
			? this.updateFromBackend() 
			: this.setState({ loading: false });
	}

	handleEdit(e) {
	}

	updateRecord(e) {
		e.disableDefault;
		var item = this.state.item;
		item.tracking_id = ReactDOM.findDOMNode(this.refs.tracking_id).children[0].value;
	    item.vendor = ReactDOM.findDOMNode(this.refs.vendor).children[0].value;
	    item.title = ReactDOM.findDOMNode(this.refs.title).children[0].value;
	    item.link = ReactDOM.findDOMNode(this.refs.link).children[0].value;
	    item.image_url = ReactDOM.findDOMNode(this.refs.image_url).children[0].value;
		this.props.routeParams.id 
			? _packageCollection.update(item)
			: _packageCollection.insert(item)
		// this.context.router.push({ pathname: '/'});
	}

    render() {
    	var edit = this.state.loading 
    	? <h1>Loading</h1>
    	: <Container className="raised very padded text segment">
    			<Header component="h1" className="dividing">Edit Record</Header>
              	<Form>
               		<Fields className="two">
					    <Field inline className="ten wide" required>
					        <label>Tracking ID</label>
					        <Input type="text" defaultValue={this.state.item.tracking_id} ref="tracking_id" onChange={this.handleEdit} fluid/>
					    </Field>
					    <Field inline className="six wide">
					        <label>Vendor</label>
					        <Input type="text" defaultValue={this.state.item.vendor} ref="vendor" onChange={this.handleEdit}  fluid/>
					    </Field>
					</Fields>
				    <Field inline>
				        <label>Description</label>
				        <Input type="text" defaultValue={this.state.item.title} fluid onChange={this.handleEdit}  ref="title" />
				    </Field>
				    <Field inline>
				        <label>Link  <a href={this.state.item.link} target="_blank"><Icon name="external"/></a></label>
			        	<Input type="text" defaultValue={this.state.item.link} fluid onChange={this.handleEdit}  ref="link" />
				    </Field>
				    <Field inline>
				        <label>Image URL</label>
			        	<Input type="text" defaultValue={this.state.item.image_url} fluid onChange={this.handleEdit}  ref="image_url" />
				    </Field>
				    <Field inline>
				        <label>Status</label>
				        <Input type="text" defaultValue={this.state.item.status} transparent readOnly fluid/>
				    </Field>
				    <Field>
             	       <Checkbox type="toggle" checked={this.state.item.state !== 'open'} readOnly>Delivered</Checkbox>
             	    </Field>
				    <Link to="/"><Button>Cancel</Button>  <Button onClick={this.updateRecord} emphasis="primary">Submit</Button></Link>
			</Form>
        </Container>;
        
        return ( edit );
    }
}

EditItem.contextTypes =  { 
	router: React.PropTypes.object.isRequired 
};

export default EditItem;
