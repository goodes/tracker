import React, { Component } from 'react';
// import { LineChart, Line, CartesianGrid, XAxis, YAxis, ComposedChart, Tooltip, Legend} from 'recharts';
import { scaleTime } from 'd3-scale';
import { timeMinute , timeDay} from 'd3-time';
import Horizon from '../horizon-container';
import moment from 'moment';
import { TimeSeries, Event } from 'pondjs';
import { Charts, ChartContainer, ChartRow, YAxis, LineChart, AreaChart, BarChart } from "react-timeseries-charts";

const _horizon = Horizon.get();
_horizon.connect();
const _sizesCollection = _horizon('sizes');

const dateFormat = (time) => {
	// console.log(moment(time).format('YYYY-MM-DD'));
	return moment(time * 1000).format('YYYY-MM-DD');
};


 const styleStampy = {
     value: {
         stroke: "#FF0000",
         strokeWidth: 2,
     }
 };

 const styleHorton = {
     value: {
         stroke: "#00FF00",
         strokeWidth: 10,
     }
 };

 const styleCal = {
     value: {
         stroke: "#0000FF",
         strokeWidth: 2,
     }
 };

const getTicks = (data) => {
	if (!data || !data.length ) {return [];}

  	return data.map(entry => entry.epo);
  const domain = [new Date(data[0].epo * 1000), new Date(data[data.length - 1].epo * 1000)];
  const scale = scaleTime().domain(domain).range([0, 1200]);
  const ticks = scale.ticks(timeDay, 1);

  // console.log(ticks)
  // return ticks;
  var res =  ticks.map(entry => +entry);
  console.log(res);
  return res;
};

const vF = (value) => {
	// console.log(value);
	return value
}

const userModel = _horizon.model(() => {
    return {
        ts: userId,
        user: horizon('users').find(userId),
        activity: {
            posts: horizon('posts').find({user: userId}),
            topComments: horizon('comments').find({user: userId}).order('rating', 'descending').limit(10)
        }
    }
});

export default class Sizes extends Component {

	constructor(props) {
        super(props);
        this.state = {
        	loading: 0,
        	stampy: null,
        	horton: null,
        	cal: null
        };
	}

	componentDidMount() {
		// console.log('Packages: componentDidMount');
		// const dt = Date("2016-09-11T00:00:0");
		const dt = new Date(2016, 7, 1, 0);
        _sizesCollection.findAll({source: 'stampy'}).above({ ts: dt}).fetch().subscribe(
            (collection) => {
                if(collection) {
                    this.setState({
                    	// data: collection, 
                    	loading: this.state.loading + 1,
                    	stampy: new TimeSeries({
    						name: "Last 3 months availability",
    						utc: false,
    						columns: ["time", "value"],
    						points: collection.map(entry => [new Date(entry.ts), entry.size/1024])
							})
                    });
                
                }
            },
            (err) => {
                console.log(err);
            }
        );
        // .above({ ts: dt})
        _sizesCollection.findAll({source: 'horton'}).above({ ts: dt}).fetch().subscribe(
            (collection) => {
                if(collection) {
                    this.setState({
                    	// data: collection, 
                    	loading: this.state.loading + 1,
                    	horton: new TimeSeries({
    						name: "Last 3 months availability",
    						utc: false,
    						columns: ["time", "value"],
    						points: collection.map(entry => [new Date(entry.ts), entry.size/1024])
							})
                    });
                
                }
            },
            (err) => {
                console.log(err);
            }
        );
        _sizesCollection.findAll({source: 'cal'}).above({ ts: dt}).fetch().subscribe(
            (collection) => {
                if(collection) {
                    this.setState({
                    	// data: collection, 
                    	loading: this.state.loading + 1,
                    	cal: new TimeSeries({
    						name: "Last 3 months availability",
    						utc: false,
    						columns: ["time", "value"],
    						points: collection.map(entry => [new Date(entry.ts), entry.size/1024])
							})
                    });
                
                }
            },
            (err) => {
                console.log(err);
            }
        );
	}

	tickFormatDate(val) {
		// console.log(val);
		// console.log(axis);
		// return dt.getDate();
		return "a"
	}
                // <i className="ui basic black label download icon"></i>

    render() {
    	console.log(this.state.loading);
        return (
        	this.state.loading < 4 
        	?  <div>
                <h1>Loading</h1>
                <div className="row">
                    <div className="eight wide column">
                      <div className="ui labeled button fluid">
                        <button className="ui basic black large fluid button">
                            File name (123 MB)
                        </button>
                        <button className="ui basic left black label"><i className="ui download icon large "></i></button>
                      </div>
                    </div>
               </div>
                <div className="row">
                    <div className="eight wide column">
                      <div className="ui labeled button">
                        <button className="ui basic black large button fluid">
                            File name with a long name (123 MB)
                        </button>
                        <button className="ui basic left black large label"><i className="ui download icon large "></i></button>
                      </div>
                    </div>
               </div>
                <div className="row">
                    <div className="eight wide column">
                      <div className="ui basic black labeled icon button">
                        <div className="ui right basic black label large"><i className="ui download icon"></i></div>
                            File name with a long name (123 MB)
                        </div>
                    </div>
               </div>
             </div>

	        : <div>
	        	<ChartContainer
	        		timeRange={this.state.stampy.timerange()}
	        		width={800}
	        		enablePanZoom={true}>
				    <ChartRow  height={350}>
				        <YAxis 
				        	id="axis1"
				        	label="GB" width="60" type="linear" 
				        	min={0} 
				        	max={Math.max(this.state.stampy.max(), this.state.horton.max(), this.state.cal.max())}/>
				        <Charts>
				            <LineChart style={styleStampy} axis="axis1" series={this.state.stampy} columns={["value"]}/>
                    <LineChart style={styleHorton} axis="axis1" series={this.state.horton} columns={["value"]}/>
                    <LineChart style={styleCal} axis="axis1" series={this.state.cal} columns={["value"]}/>
				        </Charts>
				    </ChartRow>
				</ChartContainer>
			  </div>
        );
    }
}


//<XAxis dataKey="ts" label="Date" ticks={getTicks(this.state.data)}  tickFormatter={dateFormat}/>
	    //     	<LineChart width={1200} height={600} data={this.state.data} margin={{top: 5, right: 30, left: 20, bottom: 5}}>
  			// 	<XAxis dataKey="epo" ticks={getTicks(this.state.data)} tickFormatter={dateFormat} />				
  			// 	<YAxis label="MB" tickFormatter={vF}/>
  			// 	<Tooltip/>
     //   			<Legend />
 				// <Line type="monotone" dataKey="size" dot={false} stroke="#8884d8"/>
			  // </LineChart>
