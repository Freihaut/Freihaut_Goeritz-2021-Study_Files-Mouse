// Drawing task component

import React, {Component} from 'react';

import KeyboardMouseTracker from "../KeyboardMouseTracker";
import Timer from '../LayoutComponents/Timer';

// not used in the final experiment
// import Rec from '../Images/Rec.png';
// import '../StyleSheets/BlinkingPicture.css';


const drawingMilestones = {
    "practice": [
        {x: 550, y: 315},
        {x: 550, y: 50},
        {x: 800, y: 50},
        {x: 700, y: 440},
        {x: 430, y: 250},
        ],
    "highStress" : [
        {x: 550, y: 315},
        {x: 211, y: 20},
        {x: 1039, y: 282},
        {x: 101, y: 312},
        {x: 291, y: 166},
        {x: 711, y: 200},
        {x: 845, y: 286},
        {x: 182, y: 487},
        {x: 791, y: 421},
        {x: 29, y: 405},
        {x: 50, y: 609},
        {x: 509, y: 422},
        {x: 717, y: 20},
        {x: 131, y: 484},
    ],
    "lowStress" : [
        {x: 550, y: 315},
        {x: 211, y: 20},
        {x: 1039, y: 282},
        {x: 101, y: 312},
        {x: 291, y: 166},
        {x: 711, y: 200},
        {x: 845, y: 286},
        {x: 182, y: 487},
        {x: 791, y: 421},
        {x: 29, y: 405},
        {x: 50, y: 609},
        {x: 509, y: 422},
        {x: 717, y: 20},
        {x: 131, y: 484},
    ]
};

let canvasPosition = {
    x: 0,
    y: 0
};

export default class DrawingTask extends Component {

    constructor(props) {
        super(props);
        this.state = {
            timer: false,
            touchedDrawings: 0,
            modal: "modal is-active",
            canDraw: false,
            isDrawing: false
        };

        this.handleMouseDown = this.handleMouseDown.bind(this);
        this.endTask = this.endTask.bind(this);
        this.setPosition = this.setPosition.bind(this);
        this.handleMouseUp = this.handleMouseUp.bind(this);
        this.initializeTask = this.initializeTask.bind(this);

        this.mileStones = drawingMilestones[this.props.condition];
    }

    componentDidMount() {
        window.scrollTo(0, 0);

        // Draw first line
        this.drawExample();

        // setup variable to hold store mousekeyboard data
        this.mouseKeyboardData = [];

        // Write the start message for the canDraw start
        let ctx = this.refs.canvas.getContext('2d');
        ctx.font = "17px Roboto";
        ctx.fillStyle = "hsl(171, 100%, 41%)";
        ctx.fillText("Start", 535, 340);

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

    drawExample() {
        let ctx = this.refs.canvas.getContext('2d');
        ctx.lineWidth = 6;
        ctx.strokeStyle = "hsl(0, 0%, 88%)";
        ctx.fillStyle = "hsl(0, 0%, 88%)";
        ctx.clearRect(0, 0, 1100, 630);
        // Draw the start end end circle of each segment
        for (let i = this.state.touchedDrawings; i <= this.state.touchedDrawings + 1; i += 1) {
            ctx.beginPath();
            ctx.arc(this.mileStones[i].x, this.mileStones[i].y, 7.5, 0, 2 * Math.PI);
            ctx.fill();
            ctx.stroke();
        }
        //Draw the path from circle to circle
        ctx.beginPath();
        ctx.moveTo(this.mileStones[this.state.touchedDrawings].x, this.mileStones[this.state.touchedDrawings].y);
        ctx.lineTo(this.mileStones[this.state.touchedDrawings + 1].x, this.mileStones[this.state.touchedDrawings + 1].y);
        ctx.stroke();

        //Draw a marker for the startcircle
        ctx.lineWidth = 2;
        ctx.strokeStyle = "hsl(171, 100%, 41%)";
        ctx.beginPath();
        ctx.arc(this.mileStones[this.state.touchedDrawings].x, this.mileStones[this.state.touchedDrawings].y, 8.5, 0, 2 * Math.PI);
        ctx.stroke();

    }

    setPosition(e) {
        let canvasBounds = this.refs.canvas.getBoundingClientRect();

        canvasPosition.x = e.clientX - canvasBounds.left;
        canvasPosition.y = e.clientY - canvasBounds.top;
    }

    // Draw with your mouse
    draw(e) {
        let ctx = this.refs.canvas.getContext('2d');
        if (e.buttons === 1 && this.state.canDraw) {

            ctx.beginPath(); // begin

            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.strokeStyle = "hsl(171, 100%, 41%)";

            ctx.moveTo(canvasPosition.x, canvasPosition.y); // draw from
            this.setPosition(e);
            ctx.lineTo(canvasPosition.x, canvasPosition.y); // to

            ctx.stroke(); // draw it!

        }
    }

    // Old

    // drawingProgress(e) {
    //     // If the user is canDraw
    //     if (e.buttons === 1 && this.state.canDraw) {
    //         let canvasBounds = this.refs.canvas.getBoundingClientRect();
    //         // get his mouse position
    //         let mouseX = e.clientX - canvasBounds.left;
    //         let mouseY = e.clientY - canvasBounds.top;
    //         // get the the next milestones position
    //         let circleX = this.mileStones[this.state.touchedDrawings].x;
    //         let circleY = this.mileStones[this.state.touchedDrawings].y;
    //         // calculate distance between mouse and milestone circle
    //         let dxsq = (mouseX - circleX) * (mouseX - circleX);
    //         let dysq = (mouseY - circleY) * (mouseY - circleY);
    //
    //         let distsq = dxsq + dysq;
    //         let rsq = 56.25;
    //         // If the mouse is in the circle
    //         if (distsq < rsq && this.state.touchedDrawings === 0) {
    //             // first circle touched
    //             this.setState({
    //                 touchedDrawings: this.state.touchedDrawings + 1
    //             });
    //         } else if (distsq < rsq && this.state.touchedDrawings < this.mileStones.length - 1) {
    //             // next circle touched
    //             this.drawExample();
    //             this.setState({
    //                 touchedDrawings: this.state.touchedDrawings + 1
    //             });
    //         } else if (distsq < rsq && this.state.touchedDrawings === this.mileStones.length - 1) {
    //             this.endTask();
    //         } else {
    //             // console.log("miss")
    //         }
    //     }
    // }

    // handleMovement(e) {
    //     this.draw(e);
    //     this.drawingProgress(e);
    // }

    handleMouseDown(e) {

        // if drawing has started and was stopped midway, the start is logged again
        if (this.state.canDraw) {
            this.setState({
                isDrawing: true
            })
          // if the drawing hasnt started yet
        } else {
            let canvasBounds = this.refs.canvas.getBoundingClientRect();
            // get his mouse position
            let mouseX = e.clientX - canvasBounds.left;
            let mouseY = e.clientY - canvasBounds.top;
            // get the the next milestones position
            let circleX = this.mileStones[this.state.touchedDrawings].x;
            let circleY = this.mileStones[this.state.touchedDrawings].y;
            // calculate distance between mouse and milestone circle
            let dxsq = (mouseX - circleX) * (mouseX - circleX);
            let dysq = (mouseY - circleY) * (mouseY - circleY);

            let distsq = dxsq + dysq;
            let rsq = 100; // old value 56.25

            // If the mouse is pressed inside the starting point
            if (distsq < rsq) {
                // Allow drawing to start
                this.setState({
                    canDraw: true,
                    isDrawing: true
                });
            }
        }

    }

    handleMouseUp(e) {

        // if the person is drawing
        if (this.state.canDraw) {

            let canvasBounds = this.refs.canvas.getBoundingClientRect();
            // get his mouse position
            let mouseX = e.clientX - canvasBounds.left;
            let mouseY = e.clientY - canvasBounds.top;
            // get the the next milestones position
            let circleX = this.mileStones[this.state.touchedDrawings + 1].x;
            let circleY = this.mileStones[this.state.touchedDrawings + 1].y;
            // calculate distance between mouse and milestone circle
            let dxsq = (mouseX - circleX) * (mouseX - circleX);
            let dysq = (mouseY - circleY) * (mouseY - circleY);

            let distsq = dxsq + dysq;
            let rsq = 100;

            // If the mouse is released in the end circle
            if (distsq < rsq && this.state.touchedDrawings < this.mileStones.length - 2) {
                this.setState({
                    canDraw: false,
                    isDrawing: false,
                    touchedDrawings: this.state.touchedDrawings + 1
                }, function () {
                    this.drawExample();
                });
                // if all drawings are done
            }  else if (distsq < rsq && this.state.touchedDrawings === this.mileStones.length - 2) {
                this.endTask();
                // if the mouse is released during a drawing but it is not on target
            } else {
                this.setState({
                    isDrawing: false
                })
            }
        }

    }

    // Function to end the task
    endTask(){
        this.props.proceedPhase(this.props.phaseName, this.mouseKeyboardData)
    }

    // Function for saving the mouse and keyboard usage data
    onKeyboardMouseEvent(datapoint) {

        // save tracker datapoint and add page information to it before pushing it into the data array
        // Info about the trial and whether the participant is canDraw or not
        const pageInfo = {
            page: this.props.phaseName,
            touchedMilestones: this.state.touchedDrawings,
            canDraw: this.state.canDraw,
            isDrawing: this.state.isDrawing
        };

        Object.assign(datapoint, pageInfo);
        // console.log(datapoint);
        this.mouseKeyboardData.push(datapoint);
    }

    // function to render the instruction modal before the start of the task
    renderInstructionModal() {
        return (
            <div className={this.state.modal} style={{textAlign: "left", fontSize: "18px"}}>
                <div className="modal-background">{null}</div>
                <div className="modal-content">
                    <header className="modal-card-head">
                        <p className="modal-card-title">{null}</p>
                    </header>
                    <section className="modal-card-body">
                        <div className="content">
                            <h3>Übungsaufgabe "Linie nachzeichnen"</h3>
                            <p>
                                In dieser Aufgabe geht es darum, vorgegebene Linien vom Startpunkt zum Endpunkt mit der
                                Maus nachzuzeichnen.
                            </p>
                            <p>
                                Sie können zeichnen, indem Sie ab dem Startpunkt die linke Maustaste gedrückt halten und Ihre Maus dann
                                bewegen.
                            </p>
                            <p> Der Startpunkt ist grün markiert. Folgen Sie mit Ihrer Zeichnung der vorgegebenen Linie bis zum Endpunkt und hören Sie dort
                                auf zu zeichnen, indem Sie die linke Maustaste loslassen. Falls Ihre Zeichnung im Endpunkt endet,
                                erscheint von diesem Punkt aus eine neue Linie mit dem nächsten Endpunkt.
                            </p>
                            <p>
                                Die Aufgabe ist beendet, wenn Sie alle Linien nachgezeichnet haben oder
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
        return (
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
                    <strong>Zeichnen Sie die Linien von Kreis zu Kreis nach, indem Sie die linke Maustaste gedrückt halten</strong>
                </p>
                <p style={{
                    WebkitUserSelect: "none",
                    MozUserSelect: "none",
                    msUserSelect: "none",
                    UserSelect: "none"
                }}>Zeit bis zum Abbruch: {!this.state.timer ? this.props.condition === "practice" ? "25" : "60" : <Timer time={this.props.condition === "practice" ? 25 : 60} end={()=> this.endTask()}/>}</p>
                <canvas ref="canvas"
                        style={{border: "3px solid black", marginTop: "10px"}}
                        height="630px" width="1100px"
                        onMouseMove={(e) => this.draw(e)}
                        onMouseDown={(e) => {this.setPosition(e); this.handleMouseDown(e)}}
                        onMouseEnter={this.setPosition}
                        onMouseUp={(e) => {this.handleMouseUp(e)}}>
                </canvas>
                {this.props.condition === "practice" ? this.renderInstructionModal() : null}
            </div>
        );
    }

}