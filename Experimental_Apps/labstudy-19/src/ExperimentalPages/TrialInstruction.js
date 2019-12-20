// start page of the trials

import React, {Component} from 'react';


import ProceedButton from '../LayoutComponents/ProceedButton';

export default class TrialInstruction extends Component {

    constructor(props) {
        super(props);
        this.state = {
            checked: false
        };

        this.toggleCheckBox = this.toggleCheckBox.bind(this);
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    toggleCheckBox() {
        this.state.checked ? this.setState({checked: false}) : this.setState({checked: true})
    }

    renderInstruction(props) {
      // Return the Correct Instruction Text
        if (props === "practice") {
            return(
                <div className="content">
                    <h3>Übungsblock</h3><br/>
                    <h4>Zunächst erhalten Sie die Möglichkeit, sich mit den Aufgaben in einem
                        Übungsdurchlauf vertraut zu machen.</h4>
                    <h4>Vor jeder Aufgabe erhalten Sie genaue Informationen darüber, wie Sie die
                        jeweilige Aufgabe bearbeiten sollen. Bitte lesen Sie sich diese Informationen aufmerksam durch.</h4>
                    <h4>Falls Sie Fragen zu der Bearbeitung der Aufgaben haben, wenden Sie sich bitte an die
                        Versuchsleitung. Es ist wichtig, dass Fragen im Übungsdurchgang geklärt werden, da Sie die
                        darauffolgenden Aufgaben alleine bearbeiten.</h4><br/>
                    <h4>Sobald Sie bereit sind zu beginnen, drücken Sie bitte auf "Weiter".</h4>
                    <ProceedButton onClick={() => this.props.proceedPhase()}/>
                </div>
            )
        } else if (props === "lowStress") {
            return(
                <div className="content">
                    <h3>Aufgabenblock {this.props.order === 0 ? 2 : 1}</h3><br/><br/>
                    <h4>Nun startet ein Aufgabenblock <span style={{textDecoration: "underline", fontWeight: "bolder"}}>ohne Testung Ihrer Fähigkeiten</span></h4><br/>
                    <h4>Sobald Sie bereit sind zu beginnen, drücken Sie bitte auf "Weiter".</h4>
                    <ProceedButton onClick={() => this.props.proceedPhase()}/>
                </div>
            )
        } else if (props === "highStress") {
            return (
                <div className="content">
                    <h3>Aufgabenblock {this.props.order === 0 ? 1 : 2}</h3><br/>
                    <h4>Nun startet ein Aufgabenblock <span style={{textDecoration: "underline", fontWeight: "bolder"}}>mit Testung Ihrer Fähigkeiten.</span></h4>
                    <h4><span className="has-text-danger">Hinweis:</span> Um Ihre Fähigkeiten zu testen wird während dieses Aufgabenblocks
                        Ihre Leistung automatisch erfasst, evaluiert und mit
                        Richtwerten verglichen. Sollte es Ihnen nicht gelingen, ein festgelegtes Leistungsmaß zu erfüllen,
                        erfolgt nach Abschluss des Aufgabenblocks eine weitere Prüfung Ihrer Fähigkeiten durch
                        die Versuchsleitung.</h4>
                    <h5 className="checkbox" style={{marginTop: "25px"}}>
                        <input type="checkbox" style={{marginRight: "5px"}} checked={this.state.checked} onChange={this.toggleCheckBox}/>
                        Ich habe verstanden, dass meine Leistung in diesem Aufgabenblock überprüft wird und bin bereit zu beginnen
                    </h5>
                    <ProceedButton onClick={() => this.props.proceedPhase()} disabled={!this.state.checked}/>
                </div>
            )

        }

    }

    render() {
        return (
            <div className="section">
                {this.renderInstruction(this.props.condition)}
            </div>
        );
    }

}