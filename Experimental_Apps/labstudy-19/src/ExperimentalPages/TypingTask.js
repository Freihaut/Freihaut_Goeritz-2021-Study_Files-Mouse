// Typing task component that was NOT used in the final experimental app
// shows a text and asks participants to copy the text into a text area

import React, { Component } from 'react';

// import KeyboardMouseTracker from "../KeyboardMouseTracker";
import Timer from '../LayoutComponents/Timer';

// import Rec from '../Images/Rec.png';
// import '../StyleSheets/BlinkingPicture.css';

const cardStyle = {
    width: "700px",
    marginTop: "15px",
};

const typingText = {
    "practice": "Dies ist ein Beispieltext.",
    "highStress": "Dies ist ein Platzhaltertext. Der Text für diese Bedingung ist noch unklar.",
    "lowStress": "Dies ist ein Platzhaltertext. Der Text für diese Bedingung ist noch unklar."
};

export default class WritingTask extends Component {

    constructor(props) {
        super(props);
        this.state = {
            timer: false,
            textIsCorrect: true,
            modal: "modal is-active"
        };

        this.endTask = this.endTask.bind(this);
        this.checkIfEqual = this.checkIfEqual.bind(this);
        this.initializeTask = this.initializeTask.bind(this);

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

    }


    checkIfEqual (event) {
        // get the value and length of the written text in the text field
        let writtenText = event.target.value.trim();
        let textLen = writtenText.length;

        if (writtenText === this.typeText) {
            // if the written text is the same as the text to retype, allow finishing the task
            this.setState({
                textIsCorrect: true,
            }, ()=> this.endTask())
        } else if (this.typeText.slice(0, textLen) !== writtenText) {
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

    endTask(){
        clearTimeout(this.end);
        this.props.proceedPhase(this.props.phaseName, this.mouseKeyboardData);
    }

    onKeyboardMouseEvent(datapoint) {
        // get datapoint from tracker and fill it with page relevant info before pushing it into the data array
        const pageInfo = {
            page: this.props.phaseName,
            isCorrect: this.state.textIsCorrect
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
                            <h3>Übungsaufgabe "Text abschreiben"</h3>
                            <p>
                                In dieser Aufgabe geht es darum, den vorgebenen Text exakt Wort für Wort mit allen
                                Satzzeichen in das Textfeld abzuschreiben.
                            </p>
                            <p> Wenn Sie einen Fehler machen, wird Ihnen dies angezeigt.
                                Korrigieren Sie den Fehler, bevor Sie mit dem Abschreiben fortfahren.
                            </p>
                            <p>
                                Die Aufgabe ist beendet, sobald Sie den Text korrekt abgeschrieben haben oder
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
                {/*<KeyboardMouseTracker onEvent={this.onKeyboardMouseEvent.bind(this)}/>*/}
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
                            Übrige Zeit:&nbsp;{!this.state.timer ? this.props.condition === "practice" ? "45" : "90" : <Timer time={this.props.condition === "practice" ? 45 : 90} end={()=> this.endTask()}/>}
                        </p>
                    </header>
                    <div className="card-content" style={{marginTop: "10px", textAlign: "left"}}>
                            <div className="content">
                                <p style={{fontSize: "18px",
                                    WebkitUserSelect: "none",
                                    MozUserSelect: "none",
                                    msUserSelect: "none",
                                    UserSelect: "none"}}>
                                    {this.typeText}
                                </p>
                            </div>
                            <div className="field" style={{marginRight: "5px"}}>
                                <p style={{color: "hsl(348, 100%, 61%)",
                                    visibility: this.state.textIsCorrect ? "hidden" : "visible"}}>
                                    Bitte korrigieren Sie den Fehler.
                                </p>
                                <div className="control">
                                <textarea onKeyUp={this.checkIfEqual}
                                          className={this.state.textIsCorrect ? "textarea is-link" : "textarea is-danger"}
                                          placeholder="Schreiben Sie den Text hier" rows="8">
                                </textarea>
                                </div>
                            </div>
                    </div>
                </div>
                {this.props.condition === "practice" ? this.renderInstructionModal() : null}
            </div>
        );
    }

}