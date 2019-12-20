// Typing task component

import React, { Component } from 'react';

import KeyboardMouseTracker from "../KeyboardMouseTracker";
import Timer from '../LayoutComponents/Timer';

// import Rec from '../Images/Rec.png';
// import '../StyleSheets/BlinkingPicture.css';

const cardStyle = {
    width: "700px",
    marginTop: "15px",
};

const typingText = {
    "practice": ["339540", "442590", "563757"],
    "highStress": ["141707", "724748", "269220", "341282", "399185", "520068", "937462"],
    "lowStress": ["141707", "724748", "269220", "341282", "399185", "520068", "937462"]
};

export default class PatternTyping extends Component {

    constructor(props) {
        super(props);
        this.inputRef = React.createRef();
        this.state = {
            timer: false,
            textIsCorrect: true,
            textNumber: 0,
            modal: "modal is-active"
        };

        this.renderText = this.renderText.bind(this);
        this.endTask = this.endTask.bind(this);
        this.checkIfEqual = this.checkIfEqual.bind(this);
        this.initializeTask = this.initializeTask.bind(this);
        this.checkInput = this.checkInput.bind(this);

        // Test to retype
        this.typeText = typingText[this.props.condition];
    }

    componentDidMount() {
        window.scrollTo(0, 0);

        // setup variable to hold store mousekeyboard data
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

        this.inputRef.current.focus();
    }


    checkIfEqual (event) {
        // get the value and length of the written text in the text field
        let writtenText = event.target.value.trim();
        let textLen = writtenText.length;

        if (writtenText === this.typeText[this.state.textNumber]) {
            // if the written text is the same as the text to retype, show next text or end the task
            if (this.state.textNumber < this.typeText.length - 1) {
                this.setState({
                    textIsCorrect: true,
                    textNumber: this.state.textNumber + 1
                });
                event.target.value = "";
            } else {
                this.endTask();
            }
        } else if (this.typeText[this.state.textNumber].slice(0, textLen) !== writtenText) {
            // if the the text is the same as the sliced text to retype, show no error
            this.setState({
                textIsCorrect: false,
            })
        } else {
            // if the user makes a typing mistake, show error --> set state to incorrect
            this.setState({
                textIsCorrect: true,
            })
        }

    }

    // Only allows to type in numbers on the numpad and the backspace key
    checkInput(e) {
        // check if its a numpad key or backspace key and prevent the event if it is not
        if (!(!(e.keyCode < 48 || e.keyCode > 57) || e.keyCode === 8)) {
            e.preventDefault();
        }
    }


    renderText() {
        return(this.typeText[this.state.textNumber])
    }

    endTask(){
        clearTimeout(this.end);
        this.props.proceedPhase(this.props.phaseName, this.mouseKeyboardData);
    }

    onKeyboardMouseEvent(datapoint) {
        // get datapoint from tracker and fill it with page relevant info before pushing it into the data array
        const pageInfo = {
            page: this.props.phaseName,
            isCorrect: this.state.textIsCorrect,
            taskNumber: this.state.textNumber
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
                            <h3>Übungsaufgabe "Zahlenfolge abschreiben"</h3>
                            <p>
                                In dieser Aufgabe geht es darum, die vorgebene Zahlenfolge korrekt
                                abzuschreiben.
                            </p>
                            <p>
                                Sie müssen zum Abschreiben die Zifferntasten über den Buchstaben verwenden und zur
                                Korrektur die Backspace-Taste. Benutzen Sie bei dieser Aufgabe ausschließlich Ihre rechte Hand.
                            </p>
                            <p> Wenn Sie einen Fehler machen, wird Ihnen dies angezeigt.
                                Korrigieren Sie den Fehler mit der Backspace-Taste, bevor Sie mit dem Abschreiben fortfahren.
                                Sobald Sie eine Zahlenfolge richtig und vollständig abgeschrieben haben, erscheint eine
                                neue Zahlenfolge.
                            </p>
                            <p>
                                Die Aufgabe ist beendet, sobald Sie alle Zahlenfolgen abgeschrieben haben oder
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
                <div className="card" style={cardStyle}>
                    <header className="card-header">
                        <p className="card-header-title">
                           Zeit bis zum Abbruch:&nbsp;{!this.state.timer ? this.props.condition === "practice" ? "25" : "60" : <Timer time={this.props.condition === "practice" ? 25 : 60} end={()=> this.endTask()}/>}
                        </p>
                    </header>
                    <div className="card-content" style={{marginTop: "10px"}}>
                        <div className="content">
                            <p style={{fontSize: "26px",
                                WebkitUserSelect: "none",
                                MozUserSelect: "none",
                                msUserSelect: "none",
                                UserSelect: "none"}}>
                                {this.renderText()}
                            </p>
                        </div>
                        <div className="field">
                            <p style={{color: "hsl(348, 100%, 61%)",
                                visibility: this.state.textIsCorrect ? "hidden" : "visible"}}>
                                Bitte korrigieren Sie den Fehler.
                            </p>
                            <div className="control">
                                <input style={{display: "block", margin: "auto", width: "115px", textAlign: "left"}}
                                       ref={this.inputRef}
                                       onKeyDown={this.checkInput}
                                       onKeyUp={this.checkIfEqual}
                                       className={this.state.textIsCorrect ? "input is-large is-link" : "input is-large is-danger"}/>
                            </div>
                        </div>
                    </div>
                </div>
                {this.props.condition === "practice" ? this.renderInstructionModal() : null}
            </div>
        );
    }

}