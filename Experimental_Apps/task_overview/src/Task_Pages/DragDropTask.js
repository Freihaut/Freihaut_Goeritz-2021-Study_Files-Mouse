import React, { Component } from 'react';

import KeyboardMouseTracker from '../KeyboardMouseTracker';


import DragCircle from '../Layout_Components/DragCircle';
import Timer from '../Layout_Components/Timer';


const dropTargets = [
        "green",
        "blue",
        "red",
        "blue",
        "orange",
        "green",
        "red",
        "orange",
        "blue",
        "red",
        "orange",
        "blue",
        "green",
        "blue",
        "red",
    ];


export default class DragDropTask extends Component {

    constructor(props) {
        super(props);
        this.state = {
            timer: false,
            circlesDragged: 0,
            modal: "modal is-active",
            dragging: false
        };

        this.getDragInfo = this.getDragInfo.bind(this);
        this.endTask = this.endTask.bind(this);
        this.initializeTask = this.initializeTask.bind(this);
        this.returnPositions = this.returnPositions.bind(this);
        this.renderDragCircle = this.renderDragCircle.bind(this);

        this.targets = dropTargets;
        this.key = 0;
    }

    componentDidMount() {

        window.scrollTo(0, 0);

        // setup variable to store tracker data
        this.mouseKeyboardData = [];

        // add is mounted bool to prevent set state attempts after the component is already unmounted
        this._isMounted = true;
    }

    componentWillUnmount() {
        this._isMounted = false;
    }

    initializeTask() {
        this.setState({
            modal: "modal",
            timer: true
        });
    }

    // Check if the Draggable Circle is dropped Inside the Target Circle
    returnPositions(xPos, yPos) {
        let targetX;
        let targetY;
        if(this.targets[this.state.circlesDragged] === "green") {
            targetX = 35;
            targetY = 35;
        } else if (this.targets[this.state.circlesDragged] === "orange") {
            targetX = 1060;
            targetY = 35;
        } else if (this.targets[this.state.circlesDragged] === "red") {
            targetX = 35;
            targetY = 590;
        } else if (this.targets[this.state.circlesDragged] === "blue") {
            targetX = 1060;
            targetY = 590;
        }

        let distToCircleCenter = Math.pow(targetX - xPos, 2) + Math.pow(targetY - yPos, 2);
        if (distToCircleCenter < Math.pow(10, 2)) {
            if (this.state.circlesDragged < this.targets.length - 1) {
                this.key ++;
                this.setState({
                    circlesDragged: this.state.circlesDragged + 1
                })
            } else {
                this.endTask();
            }
        } else {
            // Return the circle to its initial position
            this.key ++;
            this.setState(this.state);
        }
    }

    getDragInfo(bool) {
        if (this._isMounted) {
            if (bool){
                this.setState({dragging: true})
            } else {
                this.setState({dragging: false})
            }
        }
    }

    onKeyboardMouseEvent(datapoint) {
        // save mouse data and add pageNumber relevant info before pushing it into the data array
        // Info about the trial number and if the circle is being dragged or not
        const pageInfo = {
            page: "Drag-and-Drop Task",
            circlesDragged: this.state.circlesDragged,
            circleNumber: this.key,
            dragging: this.state.dragging
        };

        Object.assign(datapoint, pageInfo);
        this.mouseKeyboardData.push(datapoint);
    }

    renderDragCircle() {
        return(<DragCircle x="550" y="315"
                           dragging={this.getDragInfo}
                           fill={this.targets[this.state.circlesDragged]}
                           key={this.key}
                           returnPositions={this.returnPositions}/>)

    }

    endTask(){
        console.log("Tracking Data Drag-and-Drop Task:", this.mouseKeyboardData);
        this.props.toggleState();
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
                            <h3>"Drag-and-Drop Task"</h3>
                            <p>
                                This task is about dragging the colored circle inside the same colored square and dropping it there.
                            </p>
                            <p>
                                You can drag the circle by clicking on it with the left mouse button and then moving the
                                mouse to the desired position while keeping the mouse button pushed down. To drop the circle
                                release the left mouse button.
                            </p>
                            <p>
                                If you drag the circle outside of the marked playing area or drop it outside of the
                                same colored square it will reset it's position.
                            </p>
                            <p>
                                If you correctly drop the circle inside the same colored square, a new circle with a
                                different color will appear in the center of the playing area.
                            </p>
                            <p>
                                The task will end if all circles are dragged and dropped or at the end of the countdown.
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
                    <strong>Drag the circle inside the same colored square</strong>
                </p>
                <p style={{
                    WebkitUserSelect: "none",
                    MozUserSelect: "none",
                    msUserSelect: "none",
                    UserSelect: "none"
                }}>Time until task will end: {!this.state.timer ? "60" : <Timer time={60} end={()=> this.endTask()}/>}</p>
                <svg style={ {height: "630px",
                    width: "1100px",
                    border: "solid 3px black",
                    marginTop: "10px",
                    cursor: this.state.dragging ? "grabbing" : "grab"}}>
                    <rect x="10" y="10" width="50" height="50" stroke="green" strokeWidth="5px" fill="white"/>
                    <rect x="10" y="565" width="50" height="50" stroke="red" strokeWidth="5px" fill="white"/>
                    <rect x="1035" y="10" width="50" height="50" stroke="orange" strokeWidth="5px" fill="white"/>
                    <rect x="1035" y="565" width="50" height="50" stroke="blue" strokeWidth="5px" fill="white"/>
                    {this.renderDragCircle()}
                </svg>
                {this.renderInstructionModal()}
            </div>
        );
    }

}