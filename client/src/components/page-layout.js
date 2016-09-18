import React, { Component } from 'react';

export default class PageLayout extends Component {

    render() {
        return (
	        <div className="app">
                    {this.props.children}
            </div>
        );
    }
}
