// Point-and-Click Task component

import React, { Component } from 'react';

import KeyboardMouseTracker from '../KeyboardMouseTracker';
import Timer from '../LayoutComponents/Timer';

import '../StyleSheets/PointClickButtons.css';

// import Rec from '../Images/Rec.png';
// import '../StyleSheets/BlinkingPicture.css';

const taskContainerStyle = {
    height: "630px",
    width: "1100px",
    border: "solid 3px black",
    marginTop: "10px"
    // backgroundColor: "#4169E1"
};

const circlePositions = {
    "practice":
        [
            "Middle",
            0,
            "Middle",
            90,
            "Middle",
            180,
            "Middle",
            270,
            "Middle",
            360
        ],
    "highStress": [
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
    ],
    "lowStress": [
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
    ]
};

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

        this.positions = circlePositions[this.props.condition];
    }

    componentDidMount() {

        window.scrollTo(0, 0);

        // setup variable to store tracker data
        this.mouseKeyboardData = [];

        if (this.props.condition !== "practice") {
            this.initializeTask();
        }
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
        this.props.proceedPhase(this.props.phaseName, this.mouseKeyboardData);
    }

    onKeyboardMouseEvent(datapoint) {
        // save mouse data and add page relevant info before pushing it into the data array
        const pageInfo = {
            page: this.props.phaseName,
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
                            <h3>Übungsaufgabe "Kreis anklicken"</h3>
                            <p>
                                In dieser Aufgabe geht es darum, den angezeigten Kreis mit der linken Maustaste anzuklicken.
                            </p>
                            <p>
                                Sobald Sie den Kreis angeklickt haben, erscheint ein neuer Kreis.
                            </p>
                            <p> Die Aufgabe ist beendet, sobald Sie alle Kreise erfolgreich angeklickt haben oder
                                wenn der Countdown abgelaufen ist.
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
                    <strong>Klicken Sie auf den Kreis</strong>
                </p>
                <p style={{
                    WebkitUserSelect: "none",
                    MozUserSelect: "none",
                    msUserSelect: "none",
                    UserSelect: "none"
                }}>Zeit bis zum Abbruch: {!this.state.timer ? this.props.condition === "practice" ? "25" : "30" : <Timer time={this.props.condition === "practice" ? 25 : 30} end={()=> this.endTask()}/>}</p>
                <svg style={taskContainerStyle}>
                    {this.renderCircle()}
                </svg>
                {this.props.condition === "practice" ? this.renderInstructionModal() : null}
            </div>
        );
    }

}