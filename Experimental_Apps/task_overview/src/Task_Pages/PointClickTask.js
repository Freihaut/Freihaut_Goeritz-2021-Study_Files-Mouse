import React, { Component } from 'react';

import KeyboardMouseTracker from '../KeyboardMouseTracker';
import Timer from '../Layout_Components/Timer';

import '../Style_Sheets/PointClickButtons.css';


const taskContainerStyle = {
    height: "630px",
    width: "1100px",
    border: "solid 3px black",
    marginTop: "10px"
    // backgroundColor: "#4169E1"
};

const circlePositions = [
            "Middle",
            206,
            "Middle",
            92,
            "Middle",
            259,
            "Middle",
            192,
            "Middle",
            348,
            "Middle",
            207,
            "Middle",
            89,
            "Middle",
            148,
            "Middle",
            113,
            "Middle",
            347,
            "Middle",
            359,
            "Middle",
            186,
            "Middle",
            106,
        ];

export default class PointClickTask extends Component {

    constructor(props) {
        super(props);
        this.state = {
            timer: false,
            circlesClicked: 0,
            modal: "modal is-active"
        };

        this.endTask = this.endTask.bind(this);
        this.renderCircle = this.renderCircle.bind(this);
        this.clicked = this.clicked.bind(this);
        this.initializeTask = this.initializeTask.bind(this);

        this.positions = circlePositions;
    }

    componentDidMount() {

        window.scrollTo(0, 0);

        // setup variable to store tracker data
        this.mouseKeyboardData = [];

    }


    initializeTask() {
        this.setState({
            modal: "modal",
            timer: true
        });
    }


    clicked () {
        // if the circle is clicked with the number one greater than the previous clicked circle, increase circlesClicked
        // by one, if all circles are clicked, end the task
        if (this.state.circlesClicked < this.positions.length - 1) {
            this.setState({
                circlesClicked: this.state.circlesClicked + 1
            });
        } else {
            this.endTask();
        }
    }

    renderCircle() {

        let x;
        let y;

        if (this.state.circlesClicked & 1) {
            // Get a point on a circle circumference given the circle radius, the circle center point and an angle
            x = Math.cos(this.positions[this.state.circlesClicked]) * 300 + 550;
            y = Math.sin(this.positions[this.state.circlesClicked]) * 300 + 315;
        } else {
            x = 550;
            y = 315;
        }

        return(<circle
            style={{cursor: "pointer"}}
            key={this.state.circlesClicked}
            cx={x}
            cy={y}
            r="12"
            stroke="black"
            strokeWidth="1px"
            fill="LightBlue"
            onClick={() => this.clicked()}/>);

    }

    endTask(){
        console.log("Tracking Data Point-and-Click Task:", this.mouseKeyboardData);
        this.props.toggleState();
    }

    onKeyboardMouseEvent(datapoint) {
        // save mouse data and add pageNumber relevant info before pushing it into the data array
        const pageInfo = {
            page: "Point-and-Click Task",
            circlesClicked: this.state.circlesClicked
        };

        Object.assign(datapoint, pageInfo);
        this.mouseKeyboardData.push(datapoint);
    }

    renderInstructionModal(){
        return (
            <div className={this.state.modal} style={{textAlign: "left", fontSize: "18px"}}>
                <div className="modal-background">{null}</div>
                <div className="modal-content">
                    <header className="modal-card-head">
                        <p className="modal-card-title">{null}</p>
                    </header>
                    <section className="modal-card-body">
                        <div className="content">
                            <h3>"Point-and-Click Task"</h3>
                            <p>
                                This task is about clicking on the shown circle with the left mouse button.
                            </p>
                            <p>
                                As soon as a circle is clicked, it will disappear and a new circle will appear.
                            </p>
                            <p>
                                The task ends if all circles are clicked at or at the end of the countdown.
                            </p>
                        </div>
                    </section>
                    <footer className="modal-card-foot">
                        <button className="button is-link" onClick={this.initializeTask}>Start</button>
                    </footer>
                </div>
            </div>
        )
    }

    render() {
        return(
            <div>
                <KeyboardMouseTracker onEvent={this.onKeyboardMouseEvent.bind(this)}/>
                <p style={{
                    WebkitUserSelect: "none",
                    MozUserSelect: "none",
                    msUserSelect: "none",
                    UserSelect: "none"
                }}>
                    <strong>Click on the circle</strong>
                </p>
                <p style={{
                    WebkitUserSelect: "none",
                    MozUserSelect: "none",
                    msUserSelect: "none",
                    UserSelect: "none"
                }}>Time until task will end: {!this.state.timer ? "30" : <Timer time={30} end={()=> this.endTask()}/>}</p>
                <svg style={taskContainerStyle}>
                    {this.renderCircle()}
                </svg>
                {this.renderInstructionModal()}
            </div>
        );
    }

}