// Drag and Drop Task component


import React, { Component } from 'react';

import KeyboardMouseTracker from '../KeyboardMouseTracker';

// not used in the final experiment
// import Rec from '../Images/Rec.png';
// import '../StyleSheets/BlinkingPicture.css';

import DragCircle from '../LayoutComponents/DragCircle';
import Timer from '../LayoutComponents/Timer';


const dropTargets = {
    "practice":
        [
            "green",
            "orange",
            "red",
            "blue",
        ],
    "highStress": [
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
    ],
    "lowStress": [
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
    ]
};

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

        this.targets = dropTargets[this.props.condition];
        this.key = 0;
    }

    componentDidMount() {

        window.scrollTo(0, 0);

        // setup variable to store tracker data
        this.mouseKeyboardData = [];

        if (this.props.condition !== "practice") {
            this.initializeTask();
        }

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
        // save mouse data and add page relevant info before pushing it into the data array
        // Info about the trial number and if the circle is being dragged or not
        const pageInfo = {
            page: this.props.phaseName,
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
        this.props.proceedPhase(this.props.phaseName, this.mouseKeyboardData);
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
                            <h3>Übungsaufgabe "Kreis ziehen"</h3>
                            <p>
                                In dieser Aufgabe geht es darum, einen farbigen Kreis in ein gleichfarbiges quadratisches
                                Zielfeld zu ziehen und dort loszulassen (sog. Drag & Drop).
                            </p>
                            <p>
                                Sie ziehen den Kreis, in dem Sie ihn mit der linken Maustaste anklicken und dann Ihre Maus
                                mit gedrückter linker Maustaste bewegen. Um den Kreis loszulassen, lassen Sie die linke
                                Maustaste los.
                            </p>
                            <p>
                                Wenn Sie den Kreis aus Versehen außerhalb des gleichfarbigen Quadrates loslassen, kehrt
                                er an seine Ausgangsposition zurück. Der Kreis kehrt auch dann an seine Ausgangsposition
                                zurück, wenn Sie ihn außerhalb des gekennzeichneten Spielfelds ziehen.
                            </p>
                            <p>
                                Sobald der Kreis innerhalb des Quadrates mit der gleichen Farbe losgelassen wird, erscheint
                                in der Bildschirmmitte ein neuer Kreis.
                            </p>
                            <p> Die Aufgabe ist beendet, sobald Sie alle Kreise erfolgreich in das jeweilige Quadrat gezogen haben
                                oder wenn der Countdown abgelaufen ist.
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
                {/*{this.props.condition === "highStress"*/}
                {/*    ?*/}
                {/*    <figure style={{position: "absolute", top: "60px", right: "10px"}} className="image is-64x64">*/}
                {/*        <img alt={""} className={"blinkingPic"} src={Rec}/>*/}
                {/*    </figure>*/}
                {/*    :*/}
                {/*    null*/}
                {/*}*/}
                <p style={{
                    WebkitUserSelect: "none",
                    MozUserSelect: "none",
                    msUserSelect: "none",
                    UserSelect: "none"
                }}>
                    <strong>Ziehen Sie den Kreis in das Quadrat mit der gleichen Farbe</strong>
                </p>
                <p style={{
                    WebkitUserSelect: "none",
                    MozUserSelect: "none",
                    msUserSelect: "none",
                    UserSelect: "none"
                }}>Zeit bis zum Abbruch: {!this.state.timer ?
                    this.props.condition === "practice" ?
                        "25" : "60"
                    : <Timer time={this.props.condition === "practice" ? 25 : 60} end={()=> this.endTask()}/>}</p>
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
                {this.props.condition === "practice" ? this.renderInstructionModal() : null}
            </div>
        );
    }

}