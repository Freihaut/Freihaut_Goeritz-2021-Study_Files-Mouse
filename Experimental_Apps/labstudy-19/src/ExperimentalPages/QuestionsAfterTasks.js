// component that shows questions after the the end of both the high- and low-stress condition

import React, { Component } from 'react';

import ProceedButton from '../LayoutComponents/ProceedButton';

export default class StressAndSamPre extends Component {

    constructor(props) {
        super(props);
        // set a state for each questionnaire item
        this.state = {
            questions: {
                effort: -99,
                mouse_confidence: -99,
                keyboard_confidence: -99
            },
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.isQuestionnaireComplete = this.isQuestionnaireComplete.bind(this);
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    isQuestionnaireComplete() {
        // check if all questions have a value other than -99 --> each question is answered, if yes, enable proceedphase button
        for (let property in this.state.questions) {
            if (this.state.questions.hasOwnProperty(property)) {
                //console.log(property + " = " + this.state[property]);
                if (this.state.questions[property] === -99) {
                    return false;
                }
            }
        }

        return true;
    }

    handleInputChange(event) {
        // Get the name and value of the clicked radio button and save it to the corresponding question state
        const target = event.target;
        const value = target.type === "image" ? target.alt : target.value;
        const name = target.name;

        let questions = {...this.state.questions};
        questions[name] = parseInt(value);
        this.setState({questions: questions});
    }

    render() {
        return(
            <div className="section">
                <div className="content">

                    <div>
                        <h4>Beantworten Sie bitte die nachfolgenden Fragen zu den Aufgaben.</h4>
                        <hr style={{margin: "0 0", height: "3px"}}/>
                    </div>

                    <div style={{marginTop: "80px"}}>

                        <p style={{fontWeight: "bold", marginTop: "75px"}}>Ich habe mich ...</p>
                        <label style={{justifyContent: "center"}}>
                            <span style={{display: "inline-block", width: "170px", textAlign: "right"}}>gar nicht angestrengt</span><input
                            style={{width: "700px"}}
                            className="slider"
                            step="1" min="0" max="100" defaultValue="50"
                            type="range"
                            name="effort"
                            onChange={this.handleInputChange}
                        /><span>sehr angestrengt</span>
                        </label>

                        <p style={{fontWeight: "bold", marginTop: "75px"}}>Im Umgang mit der Computer-Maus finde ich mich ...</p>
                        <label style={{justifyContent: "center"}}>
                            <span style={{display: "inline-block", width: "170px", textAlign: "right"}}>sehr unsicher</span><input
                            style={{width: "700px"}}
                            className="slider"
                            step="1" min="0" max="100" defaultValue="50"
                            type="range"
                            name="mouse_confidence"
                            onChange={this.handleInputChange}
                        /><span>sehr sicher</span>
                        </label>

                        <p style={{fontWeight: "bold", marginTop: "75px"}}>Im Umgang mit der Computer-Tastatur finde ich mich ...</p>
                        <label style={{justifyContent: "center"}}>
                            <span style={{display: "inline-block", width: "170px", textAlign: "right"}}>sehr unsicher</span><input
                            style={{width: "700px"}}
                            className="slider"
                            step="1" min="0" max="100" defaultValue="50"
                            type="range"
                            name="keyboard_confidence"
                            onChange={this.handleInputChange}
                        /><span>sehr sicher</span>
                        </label>

                    </div>

                    <ProceedButton disabled={!this.isQuestionnaireComplete()} onClick={() => this.props.proceedPhase(this.props.phaseName, this.state.questions)}/>
                </div>
            </div>
        );

    }
}